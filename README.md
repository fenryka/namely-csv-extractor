# Table of Contents

<!-- ts -->
* [Namely CSV Extractor ](#namely-csv-extractor-)
    * [Purpose](#purpose)
    * [Setup](#setup)
    * [Usage](#usage)
    * [CSV RFC ](#csv-rfc-)
<!-- end -->

<!-- body-start -->

# Namely CSV Extractor 

## Purpose

Extract from Namely a (popular?) HR platform information,via the REST API, to populate CSV files in a format
understood by my [organisation chart](https://github.com/fenryka/org-chart) drawing application.

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

## Usage

replace <company> with your organisaitons namely identifier. _id est_ the one that that appears in `https://<company>.namely.com`

```
python3 namely_profile_extract.py <company>
```
## CSV RFC 

https://www.ietf.org/rfc/rfc4180.txt
