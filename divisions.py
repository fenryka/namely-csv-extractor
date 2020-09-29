import click
import pprint

from namely import Namely

# -------------------------------------------------------------------------------


def get_divisions(namely_):
    resp = namely_.get("groups")
    divisions = list(filter(lambda x: x['type'] == "Divisions", resp.json()['groups']))
    return{x['title']: x['id'] for x in divisions}


# -------------------------------------------------------------------------------


@click.command()
@click.argument("company_")
def cli(company_):
    namely = Namely.namely_login(company_)
    pprint.PrettyPrinter(indent=4).pprint(get_divisions(namely))


# -------------------------------------------------------------------------------


if __name__ == "__main__":
    cli()
