# Table of Contents

<!-- ts -->
* [Namely CSV Extractor](#namely-csv-extractor)
    * [Purpose](#purpose)
        * [Secondary Utilities](#secondary-utilities)
    * [Setup](#setup)
        * [Python complaining about dependency mismatch](#python-complaining-about-dependency-mismatch)
    * [Usage](#usage)
        * [CSV Extractor](#csv-extractor)
        * [Profile Pic Fetch](#profile-pic-fetch)
* [CSV RFC](#csv-rfc)
<!-- end -->

<!-- body-start -->

# Namely CSV Extractor

## Purpose

Extract from Namely a (popular?) HR platform information,via the REST API, to populate CSV files in a format
understood by my [organisation chart](https://github.com/fenryka/org-chart) drawing application.

### Secondary Utilities

Alongside the main script, there are a number of smaller utility scripts that may be useful

1. _namely.py_: When run from the command line will dump the full profile of the user running the script
  to the console.
2. _divisions.py_: When executed as a script will fetch all divisions for the specified company.
3. _profile_pics.py_: For each employee fetch their profile picture and write it to a file

## Setup

Create virtual environment for Python
```
virtualenv venv
source venv/bin/activate
```

Install dependencies
```commandline
pip install .
```

### Python complaining about dependency mismatch

If you get an error along the lines of

```ImportError: pycurl: libcurl link-time version (7.84.0) is older than compile-time version (7.85.0)```

It can be fixed as per the following

```
brew install curl
brew link curl --force
brew install openssl
export LIBRARY_PATH=/usr/local/opt/openssl/lib
export CPATH=/usr/local/opt/openssl/include
pip --no-cache-dir install pycurl
```

## Usage

### CSV Extractor

replace <company> with your organisaitons namely identifier. _id est_ the one that that appears in `https://<company>.namely.com`

```
python3 namely_profile_extract.py <company>
```

### Profile Pic Fetch

If your namely instance uses some SSO then you'll need to fetch the appropriate
values from stored cookies. First, navigate to namely in a web browser and
authenticate. Then, using a cookie inspector grab the values

```
# Netscape HTTP Cookie File
# http://curl.haxx.se/rfc/cookie_spec.html
# This is a generated file!  Do not edit.

<company>.namely.com	FALSE	/	TRUE	1709049313	_session_id	<<<Copy this value for param one>>>	43
<company>.namely.com	FALSE	/	FALSE	1709049311	_namely_session3	<<<Copy this value for param two>>>	68
<company>.namely.com	FALSE	/			company <company>	9
```

Usage:

```
python3 profile_pics.py <company> <session id> <namely session>
```

To dump all the profile pics into a specific directory, this can be done
with the -d flag

```
python3 profile_pics.py -d <directory> <company> <session id> <namely session>
```

# CSV RFC

For reference: https://www.ietf.org/rfc/rfc4180.txt
