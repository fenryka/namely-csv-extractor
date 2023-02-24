import abc
import os
import re
import sys
from typing import AnyStr, Dict

import click

from namely import Namely, NamelyType, NamelyPagedQuery

# -------------------------------------------------------------------------------

GroupsType = Dict[AnyStr, Dict[AnyStr, AnyStr]]

# -------------------------------------------------------------------------------


# If we find any commas (at least one) in the string, then escape it with
# wrapping quotes, first escaping extant quotes with additional quote
# marks as per the CSV RFC
def normalise(s: AnyStr) -> AnyStr:
    if s.find(',') > 0:
        s = re.sub(r'"', '""', s)

        return "\"{}\"".format(s)
    else:
        return s

# -------------------------------------------------------------------------------


def value(s: Dict, k: AnyStr) -> AnyStr:
    try:
        if s[k] is None:
            return ""
        else:
            return normalise(str(s[k]))

    except KeyError:
        return ""
    except TypeError:
        return ""

# -------------------------------------------------------------------------------


def nestedValue(s: Dict, k1: AnyStr, k2: AnyStr) -> AnyStr:
    try:
        if s[k1][k2] is None:
            return ""
        else:
            return normalise(str(s[k1][k2]))

    except KeyError:
        return ""
    except TypeError:
        return ""

# -------------------------------------------------------------------------------


class EmployeeValue(metaclass=abc.ABCMeta):
    def __init__(self, header_: AnyStr):
        self.header = header_

    @abc.abstractmethod
    def v(self, s: Dict) -> AnyStr: pass

# -------------------------------------------------------------------------------


class EmployeeIDValue (EmployeeValue):
    def __init__(self): super().__init__("Employee Id")
    def v(self, s: Dict) -> AnyStr: return value(s, "employee_id")

# -------------------------------------------------------------------------------


class EthnicityValue (EmployeeValue):
    def __init__(self): super().__init__("Ethnicity")
    def v(self, s: Dict) -> AnyStr: return value(s, "ethnicity")

# -------------------------------------------------------------------------------


class FullNameValue(EmployeeValue):
    def __init__(self): super().__init__("Full Name")
    def v(self, s: Dict) -> AnyStr: return value(s, "full_name")

# -------------------------------------------------------------------------------


class JobTitleValue (EmployeeValue):
    def __init__(self): super().__init__("Job Title")
    def v(self, s: Dict) -> AnyStr: return nestedValue(s, 'job_title', 'title')

# -------------------------------------------------------------------------------


class DivisionsValue(EmployeeValue):
    def __init__(self): super().__init__("Division")
    def v(self, s: Dict) -> AnyStr: return value(s, "Divisions")

# -------------------------------------------------------------------------------


class OfficeCityValue(EmployeeValue):
    def __init__(self): super().__init__("City")
    def v(self, s: Dict) -> AnyStr: return value(s, "Office Location City")

# -------------------------------------------------------------------------------


class TeamValue(EmployeeValue):
    def __init__(self): super().__init__("Team")
    def v(self, s: Dict) -> AnyStr: return value(s, "Team")

# -------------------------------------------------------------------------------


class OfficeLocValue(EmployeeValue):
    def __init__(self): super().__init__("Office")
    def v(self, s: Dict) -> AnyStr: return value(s, "Office Locations")

# -------------------------------------------------------------------------------


class StartDateValue (EmployeeValue):
    def __init__(self): super().__init__("Start Date")
    def v(self, s: Dict) -> AnyStr: return value(s, "start_date")

# -------------------------------------------------------------------------------


class ReportsToValue (EmployeeValue):
    def __init__(self): super().__init__("Reports To")
    def v(self, s: Dict) -> AnyStr: return value(s, "reports_to_alt")

# -------------------------------------------------------------------------------


class GenderValue (EmployeeValue):
    def __init__(self): super().__init__("Gender")
    def v(self, s: Dict) -> AnyStr: return value(s, "gender")

# -------------------------------------------------------------------------------


class SalaryValue(EmployeeValue):
    def __init__(self): super().__init__("Salary")

    def v(self, s: Dict) -> AnyStr:
        currency = nestedValue(s, 'salary', 'currency_type')
        if currency == "GBP":
            return "£" + nestedValue(s, "salary", "yearly_amount")
        elif currency == "USD":
            return "$" + nestedValue(s, "salary", "yearly_amount")
        elif currency == "EUR":
            return "€" + nestedValue(s, "salary", "yearly_amount")
        else:
            return ""

# -------------------------------------------------------------------------------


class DoBValue (EmployeeValue):
    def __init__(self): super().__init__("Date of Birth")
    def v(self, s: Dict) -> AnyStr: return value(s, "dob")

# -------------------------------------------------------------------------------


details = [
    EmployeeIDValue(),
    EthnicityValue(),
    FullNameValue(),
    JobTitleValue(),
    StartDateValue(),
    OfficeLocValue(),
    OfficeCityValue(),
    TeamValue(),
    DivisionsValue(),
    StartDateValue(),
    ReportsToValue(),
    GenderValue(),
    SalaryValue(),
    DoBValue()]

# -------------------------------------------------------------------------------


def fetchGroups(namely_: NamelyType, verbose=False) -> GroupsType:
    if verbose:
        print("Fetching groups")

    namely_groups = namely_.get("groups", ["per_page=50"], verbose)
    if not namely_groups.ok:
        raise RuntimeError()

    groupTypesById = {x['id']: x['title'] for x in namely_groups.json()['linked']['group_types']}

    return {
        v['id']: {
            'title': v['title'],
            'type': groupTypesById[v['links']['group_type']]
        } for v in namely_groups.json()['groups']
    }

# -------------------------------------------------------------------------------


def fetchProfiles(namely_: NamelyType, groups_: GroupsType, verbose=False):
    if verbose:
        print("Fetching Profiles")

    staff = {}
    query = NamelyPagedQuery(namely_)

    while True:
        res = query.getNext("profiles", ["filter[user_status]=active", "per_page=50"], verbose)

        if not res.ok:
            break
        elif res.json()['meta']['count'] == 0:
            break

        for profile in res.json()['profiles']:
            if verbose:
                try:
                    print(profile['full_name'] + ": " + profile['image']['original'])
                except TypeError:
                    pass

            staff[profile['id']] = profile
            for links in profile['links']['groups']:
                staff[profile['id']][groups_[links['id']]['type']] = groups_[links['id']]['title']

    for s in staff.values():
        try:
            s['reports_to_alt'] = staff[s['reports_to'][0]['id']]['employee_id']
        except KeyError:
            s['reports_to_alt'] = ""

    if verbose:
        print("Profiles Fetched")

    return staff

# ------------------------------------------------------------------------------


@click.command()
@click.option('--verbose', '-v', is_flag=True)
@click.option("--file", '-f', default=None, type=click.Path(exists=False))
@click.option("--replace", '-r', default=False)
@click.argument("company")
def cli(verbose, company: AnyStr, file: AnyStr, replace):
    namely = Namely.namely_login(company)

    if not file:
        file = "{}.csv".format(company)

    if not replace and os.path.exists(file):
        click.echo("Error: file already exists: '{}'".format(file), err=True)
        sys.exit(1)

    groups = fetchGroups(namely, verbose)
    staff = fetchProfiles(namely, groups, verbose)

    with open(file, 'w') as f:
        f.write(",".join(map(lambda x: x.header, details)) + os.linesep)
        for s in staff.values():
            try:
                f.write(",".join(map(lambda x: x.v(s), details)) + os.linesep)
            except TypeError:
                print("TypeError: ", end='')
                print(list(map(lambda x: x.v(s), details)))


# -------------------------------------------------------------------------------

if __name__ == "__main__":
    cli()

# -------------------------------------------------------------------------------
