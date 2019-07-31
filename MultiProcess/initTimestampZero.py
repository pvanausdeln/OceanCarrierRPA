import requests
import os
import pandas as pd

if(os.path.exists(r"C:\\Users\\alston.huang\\OneDrive - Blume Global\\UiPath\\OceanCarrierRPA\\Multiprocess\\Container_Tracking.xlsx")): # replace with correct filepath
    os.remove(r"C:\\Users\\alston.huang\\OneDrive - Blume Global\\UiPath\\OceanCarrierRPA\\Multiprocess\\Container_Tracking.xlsx") # replace with correct filepath

# if(os.path.exists(r"C:\\Users\\alston.huang\\OneDrive - Blume Global\\UiPath\\OceanCarrierRPA\\Container_Tracking.xlsx")): # replace with correct filepath
#     os.remove(r"C:\\Users\\alston.huang\\OneDrive - Blume Global\\UiPath\\OceanCarrierRPA\\Container_Tracking.xlsx") # replace with correct filepath

url = 'https://test-apps.blumesolutions.com/shipmentservice-api/v1/bv/vessel/track'
filename = 'Container_Tracking.xlsx'
r = requests.get(url, stream=True)

if r.status_code == 200:
    with open(filename, 'wb') as f:
        f.write(r.content)

# os.rename(r"C:\\Users\\alston.huang\\OneDrive - Blume Global\\UiPath\\OceanCarrierRPA\\MultiProcess\\Container_Tracking.xlsx", r"C:\\Users\\alston.huang\\OneDrive - Blume Global\\UiPath\\OceanCarrierRPA\\Container_Tracking.xlsx") # moves the API file, replace with correct filepath

df = pd.read_excel("C:\\Users\\alston.huang\\OneDrive - Blume Global\\UiPath\\OceanCarrierRPA\\Multiprocess\\" + filename)
new_df = pd.DataFrame(columns=['unitid','timestamp'])
new_df['unitid'] = df['unitid']
new_df['timestamp'] = 0
new_df.set_index('unitid', inplace=True)
new_df.to_excel("C:\\Users\\alston.huang\\OneDrive - Blume Global\\UiPath\\OceanCarrierRPA\\MultiProcess\\Timestamps.xlsx")

# os.system("python pseudoCodeScript.py")