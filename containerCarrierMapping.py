import pandas as pd
import os
from difflib import get_close_matches

mapping = {
    "ONE" : "ONE",
    "EVE" : "EVERGREEN",
    "APL" : "APL",
    "CGM" : "CGM",
    "OC2" : "OOCL"
}

carrier_prefixes = list( mapping.keys() )

# df = dataframe. object class used by pandas to represent a matrix
df = pd.read_excel(".\\..\\Container_Tracking.xlsx") #Change the path to "Container_Tracking.xlsx" if executed individually
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
    rows_df = df.loc[df['carrier'].isin( [str(str_carrier)])] #
    rows_df.set_index('unitid', inplace=True)
# finds the closest match to the keys in mapping.
# i.e. APLU-BLU would match with the "APL" key in mapping.
# play with the cutoff point range for accuracy tweaking. 0.0 - 1.0
    carrier_prefix  = get_close_matches( str(str_carrier).upper(),carrier_prefixes,1,0.4)[0]
    # creates the prefix filename. CHANGE this for additional paths.
    filename        = ".\\..\\" + mapping[carrier_prefix] + "_Container_Tracking.xlsx" #Remove the ".\\..\\" if executed individually
    if( filename not in excels ):
        excels[filename] = rows_df
    else:
        frames = [ excels[filename] , rows_df ]
        excels[filename] = pd.concat(frames)
    # print(carrier_prefix)


for filename in excels:
    if( os.path.exists( filename ) ):
        os.remove( filename )
    excels[filename].to_excel(filename)
