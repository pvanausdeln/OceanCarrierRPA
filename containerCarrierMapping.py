import pandas as pd 
import os
from difflib import get_close_matches

# ONE         = "ONE"
# EVE         = "EVE"
# APL         = "APL"
# CGM         = "CGM"
# OC2         = "OC2"

mapping = {
    "ONE" : "ONE",
    "EVE" : "EVERGREEN",
    "APL" : "APL",
    "CGM" : "CGM",
    "OC2" : "OOCL"
}

carrier_prefixes = list( mapping.keys() )

# df = dataframe. object class used by pandas to represent a matrix 
df = pd.read_excel("Container_Tracking.xlsx")
# grabs only unique carrier names
carriers = df.carrier.unique()
excels = {}

# for each carrier, filter all the rows with that carrier name
# and download them as .xlsx
for carrier in carriers:
    # might not be needed in python 3 ("i coded this in python 2.7 quickly")
    # converts from utf-8 to string 
    str_carrier = carrier.encode("utf-8")

    # returns the rows that contains a list of values in the carrier column
    rows_df = df.loc[ df['carrier'].isin( [str_carrier] ) ] #
    rows_df.set_index('unitid', inplace=True)

    carrier_prefix  = get_close_matches(str_carrier.upper(), carrier_prefixes, 1, 0.4)[0]
    filename        = mapping[carrier_prefix] + "_Container_Tracking.xlsx"
    if( filename not in excels ):
        excels[filename] = rows_df
    else:
        frames = [ excels[filename] , rows_df ]
        excels[filename] = pd.concat(frames)


for filename in excels:
    if( os.path.exists( filename ) ):
        os.remove( filename )
    excels[filename].to_excel(filename)


