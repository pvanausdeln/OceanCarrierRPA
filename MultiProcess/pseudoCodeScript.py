import requests
import os


if(os.path.exists(r"C:\\Users\\pvanausdeln\\OneDrive - Blume Global\\UiPath\\OceanCarrierRPA\\Container_Tracking.xlsx")): # replace with correct filepath
    os.remove(r"C:\\Users\\pvanausdeln\\OneDrive - Blume Global\\UiPath\\OceanCarrierRPA\\Container_Tracking.xlsx") # replace with correct filepath

url = 'https://test-apps.blumesolutions.com/shipmentservice-api/v1/bv/vessel/track'
filename = 'Container_Tracking.xlsx'
r = requests.get(url, stream=True)

if r.status_code == 200:
    with open(filename, 'wb') as f:
        f.write(r.content)

os.rename(r"C:\\Users\\pvanausdeln\\OneDrive - Blume Global\\Desktop\\Container_Tracking.xlsx", r"C:\\Users\\pvanausdeln\\OneDrive - Blume Global\\UiPath\\OceanCarrierRPA\\Container_Tracking.xlsx") # moves the API file, replace with correct filepath

#os.system("path to RPA batch file")
