# Load the libraries we need
import pandas as pd
import urllib
import time
import datetime as dt
import sys
import ast
import os     

working_directory = os.getcwd()
start_of_production = time.time()

output_directory = os.path.join(working_directory,'output')

# Create the output directory for the trip generation results
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# This option will supress the warning message on possbile copy issues - confirmed it is working as desired so turning it off
pd.set_option('chained_assignment',None)

# Get the lookup passed from the system argument
acs_data_type = sys.argv[1]
year = sys.argv[2]
api_key = sys.argv[3]
geography_lookup = ast.literal_eval(sys.argv[4])

end_5yr = int(year) - 2000
start_5yr = end_5yr - 4 

download_date = dt.datetime.today().strftime('%Y-%m-%d')
psrc_geographies = ','.join(geography_lookup.keys())

if acs_data_type == '1yr' :
    data_set = 'acs/acs1/profile'
    out_file = 'acsprof'+str(end_5yr)+'-'+str.lower(geography_lookup[psrc_geographies][2])+'-'+ str.lower(geography_lookup[psrc_geographies][1]) +'.xlsx'
    source_note = 'Source: U.S. Census Bureau, '+str(year)+' American Community Survey 1-Year Estimates'
    
elif acs_data_type == '5yr' :
    data_set = 'acs/acs5/profile'
    out_file = 'acsprof'+str(start_5yr)+'-'+str(end_5yr)+'-'+str.lower(geography_lookup[psrc_geographies][2])+'-'+ str.lower(geography_lookup[psrc_geographies][1]) +'.xlsx'
    source_note = 'Source: U.S. Census Bureau, 20'+str(start_5yr)+'-20'+str(end_5yr)+' 5-Year American Community Survey Estimates'
    
# Choose the Notes Sheet to use based on year of data
if year == '2011':
    from census_profile_notes_2011 import *

elif year == '2012':
    from census_profile_notes_2012 import *

elif year == '2013':
    from census_profile_notes_2013 import *

elif year == '2014':
    from census_profile_notes_2014 import *

elif year == '2015':
    from census_profile_notes_2015 import *

elif year == '2016':
    from census_profile_notes_2016 import *    

elif year == '2017':
    from census_profile_notes_2017 import *   
    
elif year == '2018':
    from census_profile_notes_2018 import *    
    
########################################################################################################################
########################################################################################################################

# Dictionary of output types from the dataprofiles
api_outputs = {'E':'Estimate',
               'M':'Margin of Error',
               'PE':'Percent',
               'PM':'Percent Margin of Error'}

numeric_columns = ['Estimate','Margin of Error','Percent','Percent Margin of Error']
data_tables = [['DP02','SELECTED SOCIAL CHARACTERISTICS IN THE UNITED STATES'],
               ['DP03','SELECTED ECONOMIC CHARACTERISTICS'],
               ['DP04','SELECTED HOUSING CHARACTERISTICS'],
               ['DP05','ACS DEMOGRAPHIC AND HOUSING ESTIMATES']]

##################################################################################################
##################################################################################################    
# Create an Excel object to add the tables as worksheets into - one workbook for each geography
##################################################################################################
##################################################################################################  
writer = pd.ExcelWriter(working_directory + '/output/'+out_file,engine='xlsxwriter')
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

float_format = current_workbook.add_format({'num_format': '0.00',
                                                 'align': 'center',
                                                 'bold': False})    

heading0_format = current_workbook.add_format({'bold': True,
                                               'text_wrap': False,
                                               'align': 'left'})     

heading1_format = current_workbook.add_format({'bold': False,
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

heading6_format = current_workbook.add_format({'bold': False,
                                               'text_wrap': True,
                                               'indent': 5})

heading7_format = current_workbook.add_format({'bold': False,
                                               'text_wrap': True,
                                               'indent': 5})       
notes_sheet.set_column('A:A', 120)

##################################################################################################
##################################################################################################
### Now a bunch of notes added to the Excel File
##################################################################################################
##################################################################################################
        
# General Notes of dataset that was downloaded
notes_sheet.write_string(0, 0, 'ACS dataset: ' + acs_data_type, meta_format)
notes_sheet.write_string(1, 0, 'Data Year: ' + str(year), meta_format)
notes_sheet.write_string(2, 0, 'Date of download from Census API: ' + download_date, meta_format)
notes_sheet.write_string(3, 0, 'Each tab contains a distinct data profile', meta_format)
notes_sheet.write_string(4, 0, 'Geography of Data: '+geography_lookup[psrc_geographies][1], meta_format)   
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
    
# Add in Note about Data Source    
notes_sheet.write_string(notes_row, 0, source_note, note_format) 
notes_row += 1
notes_sheet.write_string(notes_row, 0, '', note_format)
notes_row += 1

current_note = 0
for notes in dp02_notes:     
    if current_note == 0:
        notes_sheet.write_string(notes_row,0,notes,meta_format)
    else:
        notes_sheet.write_string(notes_row,0,notes,note_format)
    current_note += 1
    notes_row += 1

current_note = 0
for notes in dp03_notes:     
    if current_note == 0:
        notes_sheet.write_string(notes_row,0,notes,meta_format)
    else:
        notes_sheet.write_string(notes_row,0,notes,note_format)
    current_note += 1
    notes_row += 1

current_note = 0
for notes in dp04_notes:     
    if current_note == 0:
        notes_sheet.write_string(notes_row,0,notes,meta_format)
    else:
        notes_sheet.write_string(notes_row,0,notes,note_format)
    current_note += 1
    notes_row += 1

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
# Download the Data Profiles and store in excel
##################################################################################################
##################################################################################################  
print('Downloading a list of all variables and labels for all available data-profiles')
variable_api_call = 'https://api.census.gov/data/' + str(year) + '/'+ data_set + '/variables'
response = urllib.request.urlopen(variable_api_call)
census_data_variables = response.read()
labels_df = pd.read_json(census_data_variables)
labels_df = labels_df.rename(columns=labels_df.iloc[0]).drop(labels_df.index[0])
labels_df  = labels_df.rename(columns={'name':'variable'})
labels_df = labels_df.drop('concept',axis=1)

# Clean up the labels dataframe so it only includes data profile labels for the estimate and removes Puerto Rico specific labels
labels_df = labels_df[~labels_df['variable'].str.contains('PE')]
labels_df = labels_df[labels_df['variable'].str.contains('DP')]
labels_df = labels_df[~labels_df['variable'].str.contains('PR')]

for tables in data_tables:
    print('Downloading data-profile '+tables[0])
    
    current_profile = 'group(' + tables[0] + ')'
   
    if geography_lookup[psrc_geographies][0] == 'state':
        census_api_call = 'https://api.census.gov/data/' + str(year) + '/'+ data_set + '?get=' + current_profile + '&' + 'for='+ geography_lookup[psrc_geographies][0] +':'+ psrc_geographies + '&key=' + api_key

    elif geography_lookup[psrc_geographies][0] == 'metropolitan statistical area/micropolitan statistical area':
        census_api_call = 'https://api.census.gov/data/' + str(year) + '/'+ data_set + '?get=' + current_profile + '&for=metropolitan%20statistical%20area/micropolitan%20statistical%20area:'+psrc_geographies+ '&key=' + api_key
  
    else:
        census_api_call = 'https://api.census.gov/data/' + str(year) + '/'+ data_set + '?get=' + current_profile + '&' + 'for='+ geography_lookup[psrc_geographies][0] +':'+ psrc_geographies +'&in=state:53' + '&key=' + api_key
    
    response = urllib.request.urlopen(census_api_call)
    census_data = response.read()
    working_df = pd.read_json(census_data)
    working_df = working_df.rename(columns=working_df.iloc[0]).drop(working_df.index[0])
    working_df = pd.melt(working_df)

    # Clean up the data profiles to only include the estimate and margins of error
    working_df = working_df[~working_df['variable'].str.contains('EA')]
    working_df = working_df[~working_df['variable'].str.contains('MA')]
    working_df = working_df[~working_df['variable'].str.contains('PEA')]
    working_df = working_df[~working_df['variable'].str.contains('PMA')]
    working_df = working_df[working_df['variable'].str.contains('DP')]

    print('Adding labels and cleaning up the profile dataframe before moving to excel')
    current_df = pd.merge(working_df,labels_df,on='variable',suffixes=('_x','_y'),how='left')
    current_df['var'] = current_df.variable.str[:9]
    current_df['typ'] = current_df.variable.str[9:]
    current_df = current_df.drop('variable',axis=1)

    print('Create Clean Table format of Estimate and Margins of Error')

    for key, value in api_outputs.items():

        if key=='E':
            final_df = current_df[current_df['typ'] == key]
            final_df = final_df.drop('typ',axis=1)
            final_df  =final_df.rename(columns={'value':value})
        
        else:
            interim = current_df[current_df['typ'] == key]
            interim = interim.drop('label',axis=1)
            interim = interim.drop('typ',axis=1)
            interim  = interim.rename(columns={'value':value})
            final_df = pd.merge(final_df,interim,on='var',suffixes=('_x','_y'),how='left')

    print('Adding a field for the heading level of the variable')
    final_df['Level'] = 0
    final_df['Subject'] = ''
    final_df['Category'] = ''
    working = final_df['label']

    for i in range (0, len(working)):
        current_subject = working[i].split("!!")
        subject_items = len(working[i].split("!!"))
        final_df['Level'][i] = 'Heading' + str(subject_items - 2)
        final_df['Subject'][i] = current_subject[-1]
        final_df['Category'][i] = (current_subject[1]).upper()

    final_df = final_df.sort_values('var')
    final_df = final_df.reset_index()

    for my_columns in numeric_columns:
        final_df[my_columns] = final_df[my_columns].apply(float)    
        
    final_df['Estimate Format'] = 'integer'
    final_df['int_est'] = final_df['Estimate'].apply(int)    
    final_df['decimals'] = final_df['Estimate']-final_df['int_est']
    final_df.loc[final_df['decimals'] > 0, 'Estimate Format'] = 'float'

    final_df['MOE Format'] = 'integer'
    final_df['int_moe'] = final_df['Margin of Error'].apply(int)    
    final_df['decimals'] = final_df['Margin of Error']-final_df['int_moe']
    final_df.loc[final_df['decimals'] > 0, 'MOE Format'] = 'float'
   
    final_columns = ['Category','Subject','Estimate','Margin of Error','Percent','Percent Margin of Error','Level','Estimate Format','MOE Format']
    final_df = final_df[final_columns]  

    ##################################################################################################
    ##################################################################################################
    ### Formatting of the Excel Table of Data
    ##################################################################################################
    ##################################################################################################          
    current_worksheet = current_workbook.add_worksheet(tables[0])
        
    # Set the various final column foramts.
    current_worksheet.set_column('A:A', 2, title_format)
    current_worksheet.set_column('B:B', 60, title_format)
    current_worksheet.set_column('C:D', 16, data_format)        
    current_worksheet.set_column('E:F', 16, percentage_format)
        
    # Read in each row and format based on the contents of the level field
    heading_offset = 1
    for index, row in final_df.iterrows():
                
        # Formats for the Title Column
        if index == 0:
            current_worksheet.write(index+1, 0, row['Category'], heading0_format)
            heading_offset = heading_offset + 1
            previous_category = row['Category']

        if index > 0 and row['Category'] != previous_category:
            current_worksheet.write(index+heading_offset, 0, row['Category'], heading0_format)
            previous_category = row['Category']
            heading_offset = heading_offset + 1
        
        if row['Level'] == 'Heading0':
            current_worksheet.write(index+heading_offset, 1, row['Subject'], heading1_format)
            
        if row['Level'] == 'Heading1':
            current_worksheet.write(index+heading_offset, 1, row['Subject'], heading1_format)
            
        if row['Level'] == 'Heading2':
            current_worksheet.write(index+heading_offset, 1, row['Subject'], heading2_format)            

        if row['Level'] == 'Heading3':
            current_worksheet.write(index+heading_offset, 1, row['Subject'], heading3_format)

        if row['Level'] == 'Heading4':
            current_worksheet.write(index+heading_offset, 1, row['Subject'], heading4_format)

        if row['Level'] == 'Heading5':
            current_worksheet.write(index+heading_offset, 1, row['Subject'], heading5_format)
        
        if row['Level'] == 'Heading6':
            current_worksheet.write(index+heading_offset, 1, row['Subject'], heading6_format)
            
        if row['Level'] == 'Heading7':
            current_worksheet.write(index+heading_offset, 1, row['Subject'], heading7_format)
            
        if row['Estimate Format'] == 'float' and row['MOE Format'] == 'float':
            census_values = [['Estimate',2,float_format],['Margin of Error',3,float_format],['Percent',4,percentage_format],['Percent Margin of Error',5,percentage_format]]
                
        if row['Estimate Format'] == 'integer' and row['MOE Format'] == 'float':
            census_values = [['Estimate',2,data_format],['Margin of Error',3,float_format],['Percent',4,percentage_format],['Percent Margin of Error',5,percentage_format]]

        if row['Estimate Format'] == 'integer' and row['MOE Format'] == 'integer':
            census_values = [['Estimate',2,data_format],['Margin of Error',3,data_format],['Percent',4,percentage_format],['Percent Margin of Error',5,percentage_format]]

        if row['Estimate Format'] == 'float' and row['MOE Format'] == 'integer':
            census_values = [['Estimate',2,float_format],['Margin of Error',3,data_format],['Percent',4,percentage_format],['Percent Margin of Error',5,percentage_format]]
    
        for results in census_values:
            
            # Tests to replace error numbers with the error code
            if row[results[0]] == -555555555:
                current_worksheet.write(index+heading_offset, results[1], '*****' , results[2])

            elif row[results[0]] == -666666666:
                current_worksheet.write(index+heading_offset, results[1], '-' , results[2]) 

            elif row[results[0]] == -333333333:
                current_worksheet.write(index+heading_offset, results[1], '***' , results[2]) 

            elif row[results[0]] == -222222222:
                current_worksheet.write(index+heading_offset, results[1], '**' , results[2]) 

            elif row[results[0]] == -888888896:
                current_worksheet.write(index+heading_offset, results[1], '*****' , results[2]) 

            elif row[results[0]] == -888888888:
                current_worksheet.write(index+heading_offset, results[1], '(x)' , results[2])            

            elif row[results[0]] == -999999999:
                current_worksheet.write(index+heading_offset, results[1], 'N' , results[2])             

            elif row[results[0]] == -1000000000:
                current_worksheet.write(index+heading_offset, results[1], 'N' , results[2])

            else:
                current_worksheet.write(index+heading_offset, results[1], row[results[0]], results[2])

        if row['Percent'] >= 100:
            current_worksheet.write(index+heading_offset, 4, '(x)' , percentage_format) 

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
        
    data_title = tables[0] + ': ' + tables[1] + '\n' + str(year) + ' American Community Survey ' + acs_data_type + ' estimates, Geography: ' + geography_lookup[psrc_geographies][1]
        
    current_worksheet.set_header('&L&"Arial,Bold"'+data_title)

    final_columns = ['Category','Subject','Estimate','Margin of Error','Percent','Percent Margin of Error']
    final_df = final_df[final_columns]
        
    # Read in columns headings as the header row for the data table
    for col_num, value in enumerate(final_df.columns.values):
        current_worksheet.write(0, col_num, value, header_format)
        
    current_worksheet.merge_range('A1:B1','Subject', header_format)
  
writer.save()
end_of_production = time.time()
print ('The Total Time for all processes took', (end_of_production-start_of_production)/60, 'minutes to execute.')
exit()