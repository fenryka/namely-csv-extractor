import os
import pprint

import click
from namely import Namely, NamelyType, NamelyPagedQuery
from typing import AnyStr, Dict
import abc

# -------------------------------------------------------------------------------

GroupsType = Dict[AnyStr, Dict[AnyStr, AnyStr]]

# -------------------------------------------------------------------------------


def value(s: Dict, k: AnyStr):
    try:
        if s[k] is None:
            return ""
        else:
            return s[k]

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
            return s[k1][k2]

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
            return "£" + str(nestedValue(s, "salary", "yearly_amount"))
        elif currency == "USD":
            return "$" + str(nestedValue(s, "salary", "yearly_amount"))
        elif currency == "EUR":
            return "€" + str(nestedValue(s, "salary", "yearly_amount"))
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


def groups(namely_: NamelyType, verbose=False) -> GroupsType:
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


def profiles(namely_: NamelyType, groups_: GroupsType, verbose=False):
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
@click.argument("company_")
@click.argument("file_")
def cli(company_: AnyStr, file_: AnyStr):
    ctx = {'namely': Namely.namely_login(company_)}

    groups_ = groups(ctx['namely'], True)
    staff = profiles(ctx['namely'], groups_, True)

    with open(file_, 'w') as file:
        file.write(",".join(map(lambda x: x.header, details)) + os.linesep)
        for s in staff.values():
            try:
                file.write(",".join(map(lambda x: x.v(s), details)) + os.linesep)
            except TypeError:
                print("TypeError: ", end='')
                print(list(map(lambda x: x.v(s), details)))


# -------------------------------------------------------------------------------

if __name__ == "__main__":
    cli()

# -------------------------------------------------------------------------------
