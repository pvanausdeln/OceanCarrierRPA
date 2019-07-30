import pandas as pd 
import os

# replace .vessel with .carrier 

# df = dataframe. object class used by pandas to represent a matrix 
df = pd.read_excel("Container_Tracking.xlsx")
# grabs only unique carrier names
carriers = df.vessel.unique()

# for each carrier, filter all the rows with that carrier name
# and download them as .xlsx
for carrier in carriers:
    # might not be needed in python 3 ("i coded this in python 2.7 quickly")
    # converts from utf-8 to string 
    str_carrier = carrier.encode("utf-8")

    # returns the rows that contains a list of values in the carrier column
    rows_df = df.loc[ df['vessel'].isin( [str_carrier] ) ] #
    rows_df.set_index('unitid', inplace=True)

    # modify for where the .xlsx file should exist
    # hopefully, the values in the carrier column, match with the folder names
    filename = str_carrier.upper() + "_Container_Tracking.xlsx"
    if( os.path.exists( filename ) ):
        os.remove( filename )

    rows_df.to_excel( filename )


