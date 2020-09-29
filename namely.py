import getpass
import requests
import keyring
import pprint
import click


# -------------------------------------------------------------------------------


NAMELY_ADDRESS = target = ".namely.com/api/v1"


# -------------------------------------------------------------------------------


class Namely:
    def __init__(self, token_, company_):
        self.header = {
            'Authorization': 'Bearer {}'.format(token_),
            'Accept': "application/json"
        }
        self.address = "https://{}{}".format(company_, NAMELY_ADDRESS)

    def get(self, target_):
        return requests.get("{}/{}".format(self.address, target_), headers=self.header)

    @staticmethod
    def namely_login(company_, reset_password_=False):
        user = getpass.getuser()

        token = keyring.get_password('namely', user)

        if token is None or reset_password_:
            token = getpass.getpass("Please enter your namely API token it will be stored in your OS Keyring: ")
            keyring.set_password('namely', user, token)

        return Namely(token, company_)


# -------------------------------------------------------------------------------


@click.command()
@click.argument("company_")
def cli(company_):
    namely = Namely.namely_login(company_)
    pprint.PrettyPrinter(indent=4).pprint(namely.get("profiles/me").json())


# -------------------------------------------------------------------------------


if __name__ == "__main__":
    cli()
