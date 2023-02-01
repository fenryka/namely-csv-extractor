# Table of Contents

<!-- ts -->
* [Namely CSV Extractor](#namely-csv-extractor-)
    * [Purpose](#purpose)
    * [Usage](#usage)
<!-- te -->

# Namely CSV Extractor 

## Purpose

Extract from Namely a (popular?) HR platform information,via the REST API, to populate CSV files in a format
understood by my [organisation chart](https://github.com/fenryka/org-chart) drawing application.

## Usage

replace <company> with your organisaitons namely identifier. _id est_ the othat that appears `https://<company>.namely.com`

```
python3 namely_profile_extract.py <company>
```
