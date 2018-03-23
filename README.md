# TsunamiDataDownload
A SJTU PRP project, which can download tsunami caused by earthquake data by a button. <br>
(./TsunamiDataDownload is for reference which code by python 2 or earlier than python 3.4)<br>
(./cache is for quick demo the output of all modules and will be deleted when all works done)
## Update Information(until 2018.03.23)
### 2018.03.07 Deng
Creat this project and upload:<br> 
1. settings.py(for Input index)<br>
2. GetUsgsData.py(for get earthquake information and save it in ./cache/earthquake.csv)<br>
3. UpdateDartStation.py(for get all Dart stations' information and save them in ./cache/DartStationRecord)<br>
4. PRP_GUI.py(Demo GUI)
### 2018.03.09 Deng
Upload:<br>
1. earthquake.py(a class for earthquake)<br>
2. GetDartData(for get a certain Dart station data when a certain earthquake happened and calculate the relative time from the earthquake and the water height)<br>
3. ./cashe(for Professor to check if the modules do things correctly)<br>
fixed:<br>
1. README.md(for better record the update information)
### 2018.03.23 Zhou
Upload:<br>
1. ChooseDartStation.py(choose for five stations nearest to the earthquake.epi)<br>
### 2018.03.23 Deng
Upload:<br>
1. RemoveTidesPolynomialFit.py(Signal process part using polynomial fit)<br>
2. main.py(just run it and get the result)[partly finished]<br>
fixed:<br>
1. README.md<br>
2. bug fixed<br>
3. add two interesting result pictures(I believe DartData_52402.jpg is a Tsunami I catch for the earthquake at 2018-02-25T17:44:43.920Z)
## Future
1. Study PIL
2. Fix bugs
