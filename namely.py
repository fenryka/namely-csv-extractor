import getpass
import requests
import keyring
import pprint
import click

from typing import AnyStr, TypeVar, List


# -------------------------------------------------------------------------------


NAMELY_ADDRESS = target = ".namely.com/api/v1"

# -------------------------------------------------------------------------------


class Namely:
    def __init__(self, token_: AnyStr, company_: AnyStr):
        self.header = {
            'Authorization': 'Bearer {}'.format(token_),
            'Accept': "application/json"
        }
        self.address = "https://{}{}".format(company_, NAMELY_ADDRESS)
        self.company = company_

    def get(self, target_: AnyStr, args_=None, verbose=False):
        if args_ is None:
            args_ = []

        request = "{}/{}".format(self.address, target_)

        arg_list = "&".join(args_)
        if len(arg_list):
            request = request + "?" + arg_list

        if verbose:
            print(request)

        return requests.get(request, headers=self.header)

    @staticmethod
    def namely_login(company_: AnyStr, reset_password_=False):
        user = getpass.getuser()

        token = keyring.get_password('namely', user)

        if token is None or reset_password_:
            token = getpass.getpass("Please enter your namely API token it will be stored in your OS Keyring: ")
            keyring.set_password('namely', user, token)

        return Namely(token, company_)

# -------------------------------------------------------------------------------


NamelyType = TypeVar('NamelyType', bound=Namely)

# -------------------------------------------------------------------------------


class NamelyPagedQuery:
    def __init__(self, namely_: NamelyType):
        self.page = 0
        self.namely = namely_
        self.done = False

    def getNext(self, target_: AnyStr, args_: List, verbose=False):
        self.page = self.page + 1
        args_.append("page={}".format(self.page))
        return self.namely.get(target_, args_, verbose)

# -------------------------------------------------------------------------------


@click.command()
@click.argument("company_")
def cli(company_):
    namely = Namely.namely_login(company_)
    pprint.PrettyPrinter(indent=4).pprint(namely.get("profiles/me", []).json())

# -------------------------------------------------------------------------------


if __name__ == "__main__":
    cli()
