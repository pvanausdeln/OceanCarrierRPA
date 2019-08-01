import requests
import os
import pandas as pd

if(os.path.exists("Container_Tracking.xlsx")): # replace with correct filepath
    os.remove("Container_Tracking.xlsx") # replace with correct filepath

url = 'https://test-apps.blumesolutions.com/shipmentservice-api/v1/bv/vessel/track'
filename = 'Container_Tracking.xlsx'
r = requests.get(url, stream=True)

if r.status_code == 200:
    with open(filename, 'wb') as f:
        f.write(r.content)

df = pd.read_excel(filename)
new_df = pd.DataFrame(columns=['unitid','timestamp'])
new_df['unitid'] = df['unitid']
new_df['timestamp'] = 0
new_df.set_index('unitid', inplace=True)
new_df.to_excel("Timestamps.xlsx")

# os.system("ExecuteRobot.bat")