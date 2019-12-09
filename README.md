# Census Data Profiles
This repository contains scripts that create Census Data Profiles from the Census API for selected geogrpahies.

The Data Profiles created are:
* DP02
* DP03
* DP04
* DP05

In order for the script to run, you need have a valid census api key. If you don't have a key, go to https://api.census.gov/data/key_signup.html

## Running the script
The script should be run from the command line by launching the "census_profiles_**x**yr.bat" file. This bacth file will run the "census_data_profiles.py" file on whatever years and geographies are passed along in the batch file.
The file format is:
* python census_data_profiles.py **"1yr or 5yr"** **"year"** **"api key"** **"dictionary of place"**

Before you can launch the script, the user needs to replace the string **"enter api key"** with your valid census api key in order for the process to run. After inserting your api key into the batch file, run the file from the command line. To run the script for all the current geogrpahies used for a different year, open the  batch file and replace the **year** with your desired year.

## ACS 1 Year Data Profiles
ACS 1 year data is available for jurisdictions with a population over 65,000 people. There are currently 18 places in the Puget Sound Region with ACS 1 year data plus Washington State for a total of 19 data profiles. These 19 profiles inlcude 4 counties, 2 metropolitan statistical areas, 1 statewide summary and 12 cities. ACS 1 year data is generally released in September/October for the previous year. It takes approximately 2 minutes to downlaod and format all 19 ACS 1 year data profiles.
 
## ACS 5 Year Data Profiles
ACS 5 year data is available down to census tracts and is generally released in December. The bacth file in this repository currently pulls profiles for all cities, counties, msa's and census designated places in the Central Puget Sound Region. There are 233 of these places in the region and the script takes approximately 30 minutes to downlaod and format all 233 ACS 5 year data profiles. 

