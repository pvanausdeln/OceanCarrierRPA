import requests
import os
import subprocess
import pandas as pd
from difflib import get_close_matches
import sys

mapping = {
    "ONE" : "ONE",
	"ONEY":"ONE",
    "EVE" : "EVERGREEN",
	"EISU":"EVERGREEN",
	"APLU":"APL",
    "CGM" : "CGM",
    "COSU": "COSCO",
	"CMDU":"CGM",
    "OC2" : "OOCL",
    "OOCL": "OOCL",
	"OOLU":"OOCL",
    "MISC": "MISC"
}

if(os.path.exists(r"Container_Tracking.xlsx")): # replace with correct filepath
    os.remove(r"Container_Tracking.xlsx") # replace with correct filepath

url = 'https://apps.blumesolutions.com/shipmentservice-api/v1/bv/vessel/track'
filename = 'Container_Tracking.xlsx'
r = requests.get(url, verify=False)

if r.status_code == 200:
    with open(filename, 'wb') as f:
        f.write(r.content)

# create Timestamp.xlsx
if(len(sys.argv) > 1 and sys.argv[1] == "RESET"):
    df = pd.read_excel(filename)
    new_df = pd.DataFrame(columns=['unitid','timestamp'])
    new_df['unitid'] = df['unitid']
    new_df['timestamp'] = 0
    new_df.set_index('unitid', inplace=True)
    new_df.to_excel("Timestamps.xlsx")

TIMESTAMP_FILE = "Timestamps.xlsx"

carrier_prefixes = list( mapping.keys() )

# df = dataframe. object class used by pandas to represent a matrix
df = pd.read_excel("Container_Tracking.xlsx") #Change the path to "Container_Tracking.xlsx" if executed individually
timestamps_df = pd.read_excel(TIMESTAMP_FILE)

# left join container_tracking.xlsx with timestamp.xlsx
df = pd.merge(df, timestamps_df, left_on="unitid", right_on="unitid", how="left")
# if there are new containers, fill timestamp with 0
df.fillna(value={'timestamp':0}, inplace=True)

# if there are containers in Timestamp.xlsx that are not in Container_tracking.xlsx
# clears containers in timestamp.xlsx that are not in container_tracking.xlsx
new_timestamp_df = timestamps_df[ timestamps_df['unitid'].isin(df['unitid']) ]
new_timestamp_df.set_index('unitid', inplace=True)
if( os.path.exists(TIMESTAMP_FILE) ):
    os.remove(TIMESTAMP_FILE)
# fill empty or NaN values in timestamp column to 0
new_timestamp_df.fillna(value={'timestamp':0}, inplace=True)
new_timestamp_df.to_excel(TIMESTAMP_FILE)

# grabs only unique carrier names
carriers = df.carrier.unique()
excels = {}

# for each carrier, filter all the rows with that carrier name
# and download them as .xlsx
for carrier in carriers:

    # returns the rows that contains a list of values in the carrier column
    rows_df = df.loc[df['carrier'].isin( [str(carrier)])] #
    rows_df.set_index('unitid', inplace=True)

    # finds the closest match to the keys in mapping.
    # i.e. APLU-BLU would match with the "APL" key in mapping.
    # play with the cutoff point range for accuracy tweaking. 0.0 - 1.0
    try:
        carrier_prefix  = get_close_matches(str(carrier).upper(), carrier_prefixes, 1, 0.4)[0]
    except Exception as e:
        print(e)
        print("COULD NOT FIND CARRIER FOR " + carrier)
        carrier_prefix = "MISC"

    # creates the prefix filename. CHANGE this for additional paths.
    filename = mapping[carrier_prefix] + "_Container_Tracking.xlsx" #Remove the ".\\..\\" if executed individually
    if( filename not in excels ):
        excels[filename] = rows_df
    else:
        frames = [ excels[filename] , rows_df ]
        excels[filename] = pd.concat(frames)


for filename in excels:
    if( os.path.exists( filename ) ):
        os.remove( filename )
    # excels[filename].drop_duplicates(inplace=True)
    excels[filename].to_excel(filename)
