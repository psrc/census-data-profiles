# This script creates Data Profiles from the Census API
# Created by Puget Sound Regional Council Staff

# Load the libraries we need
import pandas as pd
import urllib
import time
import datetime as dt     

from census_profile_descriptions import *
from census_profile_notes import *

download_date = dt.datetime.today().strftime('%Y-%m-%d')
psrc_geographies = ','.join(geography_lookup.keys())
geography_ids = psrc_geographies.split(",")

# Functions to Download and Format Census API datatables
def create_census_url(data_set, data_tables, geography, type_of_geography, year, api_key):

    if type_of_geography == 'state':
        census_api_call = 'https://api.census.gov/data/' + str(year) + '/'+ data_set + '?get=' + data_tables + '&' + 'for='+ type_of_geography +':'+ geography + '&key=' + api_key    

    elif type_of_geography == 'metropolitan statistical area/micropolitan statistical area':
        census_api_call = 'https://api.census.gov/data/'+ str(year) +'/'+ data_set +'?get='+ data_tables + '&for=metropolitan%20statistical%20area/micropolitan%20statistical%20area:'+geography+ '&key=' + api_key
  
    else:
        census_api_call = 'https://api.census.gov/data/' + str(year) + '/'+ data_set + '?get=' + data_tables + '&' + 'for='+ type_of_geography +':'+ geography +'&in=state:53' + '&key=' + api_key
    
    return census_api_call

def download_census_data(data_url):

    response = urllib.request.urlopen(data_url)
    census_data = response.read()
    
    return census_data

def format_census_tables(census_download, working_table, updated_names, working_geography):
    working_df = pd.read_json(census_download)
    working_df = working_df.rename(columns=working_df.iloc[0]).drop(working_df.index[0])
    
    if working_geography == 'metropolitan statistical area/micropolitan statistical area':
        working_df = working_df.drop([working_geography],axis=1)
    
    else:
        working_df = working_df.drop(['state',working_geography],axis=1)
    
    working_df['DataTable'] = working_df.columns[0]
    working_df['DataTable'] = working_df['DataTable'].map(lambda x: str(x)[:-1])  
    my_table = working_df.iloc[0]['DataTable'] 
    working_df['Subject'] = working_table[my_table][0]
    working_df['Level'] = working_table[my_table][1]
    working_df.columns = updated_names
            
    return working_df

# Download and process the Census tables / data profiles
start_of_production = time.time()

for analysis_geography in geography_ids:

    ##################################################################################################
    ##################################################################################################    
    # Create an Excel object to add the tables as worksheets into - one workbook for each geography
    ##################################################################################################
    ##################################################################################################  

    writer = pd.ExcelWriter(working_directory + '/output/acs-'+acs_data_type+'-profile-'+data_year+'-'+geography_lookup[analysis_geography][2]+'-'+ geography_lookup[analysis_geography][1]+'.xlsx',engine='xlsxwriter')
    current_workbook  = writer.book
    notes_sheet = current_workbook.add_worksheet('Notes')

    ##################################################################################################
    ##################################################################################################
    ###  A bunch of cell formats for the final excel files
    ### Needs to be here since they are objects passed to the workbook object
    ##################################################################################################
    ##################################################################################################
    
    meta_format = current_workbook.add_format({'bold': True,
                                             'text_wrap': True,
                                             'align': 'justify',
                                             'fg_color': '#D7E4BC'})

    note_format = current_workbook.add_format({'bold': False,
                                             'text_wrap': True,
                                             'indent': 2,
                                             'align': 'justify',
                                             'fg_color': '#D7E4BC'})

    header_format = current_workbook.add_format({'bold': True,
                                             'text_wrap': True,
                                             'align': 'center',
                                             'fg_color': '#D7E4BC',
                                             'border': 1})
        
    title_format = current_workbook.add_format({'bold': True,
                                             'text_wrap': True,
                                             'align': 'justify'})

    data_format = current_workbook.add_format({'num_format': '#,##0',
                                               'align': 'center',
                                               'bold': False})

    percentage_format = current_workbook.add_format({'num_format': '0.0',
                                                     'align': 'center',
                                                     'bold': False})

    heading1_format = current_workbook.add_format({'bold': True,
                                                   'text_wrap': True,
                                                   'align': 'justify'})    

    heading2_format = current_workbook.add_format({'bold': False,
                                                   'text_wrap': True,
                                                   'indent': 1})         

    heading3_format = current_workbook.add_format({'bold': False,
                                                   'text_wrap': True,
                                                   'indent': 2})  

    heading4_format = current_workbook.add_format({'bold': False,
                                                   'text_wrap': True,
                                                   'indent': 3}) 

    heading5_format = current_workbook.add_format({'bold': False,
                                                   'text_wrap': True,
                                             'indent': 4}) 

    notes_sheet.set_column('A:A', 120) 

    ##################################################################################################
    ##################################################################################################
    ### Now a bunch of notes added to the Excel File
    ##################################################################################################
    ##################################################################################################
        
    # General Notes of dataset that was downloaded
    notes_sheet.write_string(0, 0, 'ACS dataset: ' + acs_data_type, meta_format)
    notes_sheet.write_string(1, 0, 'Data Year: ' + str(data_year), meta_format)
    notes_sheet.write_string(2, 0, 'Date of download from Census API: ' + download_date, meta_format)
    notes_sheet.write_string(3, 0, 'Each tab contains a distinct data profile', meta_format)
    notes_sheet.write_string(4, 0, 'Geography of Data: '+geography_lookup[analysis_geography][1], meta_format)   
    notes_sheet.write_string(5, 0, '', meta_format)
    
    notes_row = 6
    
    # Add in Symbol Related Notes
    current_note = 0
    for notes in symbol_notes:     
        if current_note == 0:
            notes_sheet.write_string(notes_row,0,notes,meta_format)
        else:
            notes_sheet.write_string(notes_row,0,notes,note_format)
        current_note += 1
        notes_row += 1

    # Add in General Data Profile Notes
    current_note = 0
    for notes in all_profile_notes:     
        if current_note == 0:
            notes_sheet.write_string(notes_row,0,notes,meta_format)
        else:
            notes_sheet.write_string(notes_row,0,notes,note_format)
        current_note += 1
        notes_row += 1
    
    for tables in census_tables:
        
        print ('Working on ', geography_lookup[analysis_geography][1] , ' data profile ' , tables[1])
        
        # First place some notes specific to the Census Table in the Notes page
        if tables[1] == 'DP02':
            current_note = 0
            for notes in dp02_notes:     
                if current_note == 0:
                    notes_sheet.write_string(notes_row,0,notes,meta_format)
                else:
                    notes_sheet.write_string(notes_row,0,notes,note_format)
                current_note += 1
                notes_row += 1

        if tables[1] == 'DP03':
            current_note = 0
            for notes in dp03_notes:     
                if current_note == 0:
                    notes_sheet.write_string(notes_row,0,notes,meta_format)
                else:
                    notes_sheet.write_string(notes_row,0,notes,note_format)
                current_note += 1
                notes_row += 1

        if tables[1] == 'DP04':
            current_note = 0
            for notes in dp04_notes:     
                if current_note == 0:
                    notes_sheet.write_string(notes_row,0,notes,meta_format)
                else:
                    notes_sheet.write_string(notes_row,0,notes,note_format)
                current_note += 1
                notes_row += 1

        if tables[1] == 'DP05':
            current_note = 0
            for notes in dp05_notes:     
                if current_note == 0:
                    notes_sheet.write_string(notes_row,0,notes,meta_format)
                else:
                    notes_sheet.write_string(notes_row,0,notes,note_format)
                current_note += 1
                notes_row += 1

        ##################################################################################################
        ##################################################################################################
        ### Download the Census Data Tables and store in a dataframe
        ##################################################################################################
        ##################################################################################################  

        # create a blank dataframe sized based on the number of columns in the census output we want
        new_df = pd.DataFrame(columns=column_names)
        
        # Create the list of census variables to pass to the census API and collect the data
        for key, value in tables[2].items():
            census_data= key +'E',key +'M',key +'PE',key +'PM'
       
            # Create the query and do the census api call to collect the data in json format
            census_data = ','.join(census_data)
            url_call = create_census_url(tables[0], census_data, analysis_geography, geography_lookup[analysis_geography][0], data_year, my_key)
            downloaded_data = download_census_data(url_call)
            current_df = format_census_tables(downloaded_data, tables[2],column_names,geography_lookup[analysis_geography][0])
            
            new_df = new_df.append(current_df)

        new_df = new_df.sort_values('DataTable')
        new_df = new_df.reset_index()
        
        for my_columns in numeric_columns:
            new_df[my_columns] = new_df[my_columns].apply(float)

        ##################################################################################################
        ##################################################################################################
        ### Formatting of the Excel Table of Data
        ##################################################################################################
        ##################################################################################################          
        # Create a worksheet object for each data table
        current_worksheet = current_workbook.add_worksheet(tables[1])
        
        # Set the various final column foramts.
        current_worksheet.set_column('A:A', 60, title_format)
        current_worksheet.set_column('B:C', 16, data_format)        
        current_worksheet.set_column('D:E', 16, percentage_format)
        
        # Read in each row and format based on the contents of the level field
        for index, row in new_df.iterrows():
            
            # Formats for the Title Column
            if row['Level'] == 'Heading1':
                current_worksheet.write(index+1, 0, row['Subject'], heading1_format)
            
            if row['Level'] == 'Heading2':
                current_worksheet.write(index+1, 0, row['Subject'], heading2_format)            

            if row['Level'] == 'Heading3':
                current_worksheet.write(index+1, 0, row['Subject'], heading3_format)

            if row['Level'] == 'Heading4':
                current_worksheet.write(index+1, 0, row['Subject'], heading4_format)

            if row['Level'] == 'Heading5':
                current_worksheet.write(index+1, 0, row['Subject'], heading5_format)
                
            census_values = [['Estimate',1,data_format],['Margin of Error',2,data_format],['Percent',3,percentage_format],['Percent Margin of Error',4,percentage_format]]
            
            for results in census_values:
            
                # Tests to replace error numbers with the error code
                if row[results[0]] == -555555555:
                    current_worksheet.write(index+1, results[1], '*****' , results[2])

                elif row[results[0]] == -888888896:
                    current_worksheet.write(index+1, results[1], '*****' , results[2]) 

                elif row[results[0]] == -888888888:
                    current_worksheet.write(index+1, results[1], '(x)' , results[2])            

                elif row[results[0]] == -999999999:
                    current_worksheet.write(index+1, results[1], 'N' , results[2])             

                elif row[results[0]] == -1000000000:
                    current_worksheet.write(index+1, results[1], 'N' , results[2])

                else:
                    current_worksheet.write(index+1, results[1], row[results[0]], results[2])

            if row['Percent'] >= 100:
                current_worksheet.write(index+1, 3, '(x)' , percentage_format) 
                
        ##################################################################################################
        ##################################################################################################
        ### Formatting of the Excel Header, Footer and Print Options
        ##################################################################################################
        ##################################################################################################   
        # Format the printed pages
        notes_sheet.set_paper(1)
        notes_sheet.set_portrait()
        notes_sheet.fit_to_pages(1, 1)       
        notes_sheet.set_footer('&LPage &P of &N &R&D')
        notes_sheet.repeat_rows(0)

        current_worksheet.set_paper(1)
        current_worksheet.set_portrait()
        current_worksheet.fit_to_pages(1, 0)       
        current_worksheet.set_footer('&LPage &P of &N &R&D')
        current_worksheet.repeat_rows(0)
        
        data_title = tables[1] + ': ' + tables[3] + '\n' + str(data_year) + ' American Community Survey ' + acs_data_type + ' estimates \n' + 'Geography: ' + geography_lookup[analysis_geography][1] +' \n'
        
        current_worksheet.set_header('&L&"Arial,Bold"'+data_title)

        final_columns = ['Subject','Estimate','Margin of Error','Percent','Percent Margin of Error']
        final_df = new_df[final_columns]
        
        # Read in columns headings as the header row for the data table
        for col_num, value in enumerate(final_df.columns.values):
            current_worksheet.write(0, col_num, value, header_format) 
  
    writer.save()

end_of_production = time.time()
print ('The Total Time for all processes took', (end_of_production-start_of_production)/60, 'minutes to execute.')