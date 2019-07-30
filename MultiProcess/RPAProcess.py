import requests
import os
import subprocess


if(os.path.exists(r"C:\\Users\\pvanausdeln\\OneDrive - Blume Global\\UiPath\\OceanCarrierRPA\\MultiProcess\\Container_Tracking.xlsx")): # replace with correct filepath
    os.remove(r"C:\\Users\\pvanausdeln\\OneDrive - Blume Global\\UiPath\\OceanCarrierRPA\\MultiProcess\\Container_Tracking.xlsx") # replace with correct filepath

url = 'https://test-apps.blumesolutions.com/shipmentservice-api/v1/bv/vessel/track'
filename = 'Container_Tracking.xlsx'
r = requests.get(url, stream=True)

if r.status_code == 200:
    with open(filename, 'wb') as f:
        f.write(r.content)

os.system("python containerCarrierMapping.py")

#Add the path to UiRobot.exe as an env variable before executing the below command
os.system(r".\\ExecuteRobot.bat")
