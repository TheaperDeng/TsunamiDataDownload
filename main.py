from earthquake import Earthquake
from GetUsgsData import GetUsgsData
from GetDartData import GetDartData
from ChooseDartStation import ChooseDartStation
from settings import Settings
from RemoveTidesPolynomialFit import RemoveTidesPolynomialFit
from UpdateDartStation import UpdateDartStation

def test():
    Earthquake_Settings=Settings()
    GetUsgsData(Earthquake_Settings)
    earthquake=Earthquake()
    earthquake.initfrom('./cache/earthquake.csv',1)
    UpdateDartStation()
    tar_station=ChooseDartStation(earthquake)
    for stationnum in tar_station:
        try:
            GetDartData(stationnum,earthquake)
            filename="./cache/DartData_"+stationnum+".csv"
            RemoveTidesPolynomialFit(filename)
        except:
            print("Sorry,no data for station",stationnum)
            continue
    
test()