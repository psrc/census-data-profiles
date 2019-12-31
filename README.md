# Census Data Profiles
This repository contains scripts that create Census Data Profiles from the Census API for the Puget Sound Region.

The Data Profiles created are:
* DP02
* DP03
* DP04
* DP05

In order for the script to run, you need have a valid census api key. If you don't have a key, go to https://api.census.gov/data/key_signup.html

## Running the script
The script should be run from the command line by launching the "run_profiles.bat" file. This bacth file will run the "census_data_profiles.py" file on whatever years and ACS types (1yr or 5yr) are passed along in the batch file.
The file format is:
* python census_data_profiles.py **"1yr or 5yr"** **"year"** **"api key"**

Before you can launch the script, the user needs to replace the string **"enter api key"** with your valid census api key in order for the process to run. After inserting your api key into the batch file, run the file from the command line. To run the script for a different year, open the  batch file and replace the **year** with your desired year.

## Place Shapefiles
The script downloads all places for any given year within Washington State via the Census API. To limit the output files to places within the PSRC Region, a spatial join is performed in the script using Census Place shapefiles by year that are downloaded and written to the user's download folder. All files are removed after script completion.