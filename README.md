# airbnb_scrape_analysis
Webscraping and analyzing airbnb data

# Getting Started
Requires selenium Chrome webdriver
<code>sudo apt install chromium-chromedriver </code>

## Environment Setup

```shell
python3 -m venv ENVIRONMENT_PATH
```
Example `python3 -m venv ./venv`

Activate the virtual environment
```shell
source ./venv/bin/activate
```

The requirements.txt file contains a list of the dependencies and versions required for running the app. The following command will install the packages according to the requirements.txt configuration file.
```
pip install -r requirements.txt
```

## Running Application
From the command line, module accepts city name and state as arguments. Multi-word cities should be separated by a hyphen. Country Name defaults to 'United-States', but can be edited in script. 

```
python airbnb_webscrape.py San-Diego ca
```

# Attributes returned in CSV for each listing
  - Title
  - Dwelling type
  - Location
  - Price
  - Number of Guests the listing can accomodate
  - Number of Bedrooms
  - Number of Beds
  - Number of Bathrooms
  - Top 4 listed amenities
  - Listing Url
  
