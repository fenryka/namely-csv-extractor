import click

from namely import Namely
from divisions import get_divisions

from typing import AnyStr, ClassVar

# -------------------------------------------------------------------------------


def load_division(namely_: ClassVar, division_: AnyStr, division_id_: AnyStr):
    resp = namely_.get("groups/{}".format(division_id_))

    all_employees = list(filter(lambda x: x['user_status'] == "active", resp.json()['groups'][0]['linked']['profiles']))

    employees = {y['id']: {'name': y['full_name']} for y in all_employees}

    #
    # This totally sucks that we have to grab each
    #
    for employee_id, info in employees.items():
        resp = namely_.get("profiles/{}".format(employee_id))

        employees[employee_id]['location'] = (list(filter(
            lambda x: x['type'] == "Office Location City", resp.json()['linked']['groups']))[0]['title'])

        employees[employee_id]['manager'] = resp.json()['profiles'][0]['reports_to'][0]
        employees[employee_id]['internalID'] = resp.json()['profiles'][0]['employee_id']
        employees[employee_id]['job_title'] = resp.json()['profiles'][0]['job_title']['title'].strip()
        employees[employee_id]['ethnicity'] = resp.json()['profiles'][0]['ethnicity']

        try:
            employees[employee_id]['gender'] = resp.json()['profiles'][0]['gender']
        except KeyError:
            employees[employee_id]['gender'] = "UNKNOWN"

    file = open("{}.csv".format(division_.replace(" ", "-")), "w")

    file.write("Employee ID,Name,Location,Supervisor ID,Gender,Job Title,Division,Ethnicity\n")
    for employee in employees.values():
        line = "{},{},{},{},{},{},{},{}".format(
            employee['internalID'].strip(),
            employee['name'],
            employee['location'],
            employees.get(employee['manager']['id'], {'internalID': ""})['internalID'],
            employee['gender'],
            employee['job_title'].strip(),
            division_,
            employee['ethnicity'])

        file.write("{}\n".format(line))


# -------------------------------------------------------------------------------


@click.group()
@click.argument("company_")
@click.pass_context
def cli(ctx, company_):
    if not ctx.obj:
        ctx.obj = {}

    ctx.obj['namely'] = Namely.namely_login(company_)
    ctx.obj['divisions'] = get_divisions(ctx.obj['namely'])


# -------------------------------------------------------------------------------


@cli.command()
@click.pass_context
def company(ctx):
    for k, v in ctx.obj['divisions'].items():
        click.echo("Loading {}".format(k))
        load_division(ctx.obj['namely'], k, v)

# -------------------------------------------------------------------------------


@cli.command()
@click.argument("division_")
@click.pass_context
def division(ctx, division_):
    divisions = ctx.obj['divisions']
    if division_ not in divisions:
        click.echo("Unknown division {}, valid options [{}]".format(division_, ",".join(divisions.keys())))

    load_division(ctx.obj['namely'], division_, divisions[division_])


# -------------------------------------------------------------------------------


if __name__ == "__main__":
    cli(obj={})
