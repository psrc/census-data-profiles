# Census Data Profiles
This repository contains scripts that create Census Data Profiles from the Census API for selected geogrpahies.

The Data Profiles created are specified in the census_profile_descriptions file and default to:
* DP02
* DP03
* DP04
* DP05

In order for the script to run, you need have a valid census api key. If you don't have a key, go to https://api.census.gov/data/key_signup.html

The script should be run from the command line by launching the "census_profiles.bat" file. This bacth file will run the "census_data_profiles.py" file on whatever years and geographies and passed along in the batch file.
The file format is:
* python census_data_profiles_1yr.py 1yr **year** **api key** **dictionary of place**
* python census_data_profiles_5yr.py 5yr **year** **api key** **dictionary of place**
	
To run the script for all the current geogrpahies used for the 1yr ACS for a different year, open the _1yr batch file and replace the year value with your current year.
 

