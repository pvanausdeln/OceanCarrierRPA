:Schedule
::The below runs the RPAProcess.py script

python RPAProcess.py

::Change directory to where UiRobot.exe is located

cd C:\Users\sowrab.iyengar\AppData\Local\UiPath\app-19.7.0

::Run the UiRobot.exe with the file name as an argument, also change directory to your xaml file 

UiRobot.exe -file C:\Users\sowrab.iyengar\Documents\OceanCarrierRPA\MultiProcess\OceanCarrierRPAWithNames.xaml

::Change directory back to "Multiprocess" folder
cd C:\Users\sowrab.iyengar\Documents\OceanCarrierRPA\MultiProcess

::Run it after an hour again

timeout /t 3600 /nobreak

goto :Schedule