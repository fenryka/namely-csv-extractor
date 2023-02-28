import click
import pycurl
import certifi

from typing import AnyStr
from namely import Namely, NamelyType, NamelyPagedQuery

# -------------------------------------------------------------------------------


image_url = 'https://{}.namely.com/utils/profile_thumbnails'

# -------------------------------------------------------------------------------


def fetchProfilesPicURLS(namely_: NamelyType, session_id, namely_session, directory=".", verbose=False):
    if verbose:
        print("Fetching Profiles")

    query = NamelyPagedQuery(namely_)

    while True:
        res = query.getNext("profiles", ["filter[user_status]=active", "per_page=50"], verbose)

        if not res.ok:
            break
        elif res.json()['meta']['count'] == 0:
            break

        for profile in res.json()['profiles']:
            try:
                with open('{}/{}.jpg'.format(directory, profile['full_name'].replace(" ", "_")), 'wb') as f:
                    c = pycurl.Curl()
                    c.setopt(c.URL, "{}/{}/200".format(image_url.format(namely_.company), profile['id']))
                    c.setopt(c.WRITEDATA, f)
                    c.setopt(c.CAINFO, certifi.where())
                    c.setopt(c.FOLLOWLOCATION, True)
                    c.setopt(c.VERBOSE, True)
                    c.setopt(c.COOKIE, '_session_id={}; _namely_session3={}'.format(session_id, namely_session))
                    c.perform()
                    c.close()

            except TypeError:
                pass

# ------------------------------------------------------------------------------


@click.command()
@click.option('--verbose', '-v', is_flag=True)
@click.option('--directory', '-d', default=".", type=click.Path(exists=True))
@click.argument("company")
@click.argument("session_id")
@click.argument("namely_session")
def cli(verbose, directory, company: AnyStr, session_id: AnyStr, namely_session: AnyStr):
    namely = Namely.namely_login(company)

    fetchProfilesPicURLS(namely, session_id, namely_session, directory, verbose)

# -------------------------------------------------------------------------------


if __name__ == "__main__":
    cli()

# -------------------------------------------------------------------------------
