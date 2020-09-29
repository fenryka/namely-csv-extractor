# Table of Contents

<!-- ts -->
* [Namely CSV Extractor ](#namely-csv-extractor-)
    * [Purpose](#purpose)
    * [Usage](#usage)
    * [ToDO](#todo)
<!-- te -->

# Namely CSV Extractor 

## Purpose

Extract from Namely a (popular?) HR platform informaiton,via the REST API, to populate CSV files in a format
understood by my [organisation chart](https://github.com/fenryka/org-chart) drawing application.

## Usage

replace <company> with your organisaitons namely identifier. _id est_ the othat that appears `https://<company>.namely.com`

```
python3 division_to_csv.py <company> division <internal division>
python3 division_to_csv.py <company> company
```

## ToDO

1. This could make much better use of the paginated /profiles endpoint since right now
   its super slow as it's making an individaul request per employee
1. Error handling, right now there is very very little
