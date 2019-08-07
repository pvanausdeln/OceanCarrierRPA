:Schedule
::The below runs the RPAProcess.py script

cd %~dp0

python RPAProcess.py

::Change directory to where UiRobot.exe is located
pushd .

set multi=%cd%

cd %USERPROFILE%\AppData\Local\UiPath\app-19.7.0

::Run the UiRobot.exe with the file name as an argument, also change directory to your xaml file 

UiRobot.exe -file "%multi%\OceanCarrierRPAWithNames.xaml"

::Change directory back to "Multiprocess" folder
popd

::Run it after an hour again

timeout /t 3600 /nobreak

goto :Schedule