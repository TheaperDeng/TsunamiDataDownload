#!/usr/bin/python3
# -*- coding:utf-8 -*-

'''Choose the first [num_of_statin] nearest to the earthquake location'''

__author__ = 'Junwei Deng & Runqing Zhou'

import csv
import os
import re
import math
from earthquake import Earthquake

def ChooseDartStation(earthquake,num_of_station):
    #You can use the function just as following:
        # earthquake=Earthquake()
        # earthquake.initfrom('./cache/earthquake.csv',1)   
        # ChooseDartStation(earthquake,100)
    with open("./cache/DartStationRecord.csv","r",encoding="utf-8")as g:
        lines_station=g.readlines()
        ang_list=[50]
        for i in range(1,len(lines_station)):
            ang=math.acos(math.sin(float(earthquake.epi[1])/180*math.pi)*math.sin(float(lines_station[i].split(',')[2])/180*math.pi)+math.cos(float(earthquake.epi[1])/180*math.pi)*math.cos(float(lines_station[i].split(',')[2])/180*math.pi)*math.cos(float(earthquake.epi[0])/180*math.pi - float(lines_station[i].split(',')[1])/180*math.pi))
            #lines_station[i]=lines_station[i]+','+str(ang)
            ang_list.append(ang)
            #print(ang)
        station_num1=lines_station[ang_list.index(min(ang_list))].split(',')[0]
        targetstation=[station_num1]
        for i in range(1,num_of_station):
            ang_list[ang_list.index(min(ang_list))]=50
            station_num=lines_station[ang_list.index(min(ang_list))].split(',')[0]
            if (station_num=='StationNumber'):
                break
            targetstation.append(station_num)
        return targetstation
        g.close()
        
def ChooseiocStation(earthquake,num_of_station):
    with open("./cache/iocStationRecord.csv","r",encoding="utf-8")as g:
        lines_station=g.readlines()
        ang_list=[50]
        for i in range(1,len(lines_station)):
            ang=math.acos(math.sin(float(earthquake.epi[1])/180*math.pi)*math.sin(float(lines_station[i].split(',')[2])/180*math.pi)+math.cos(float(earthquake.epi[1])/180*math.pi)*math.cos(float(lines_station[i].split(',')[2])/180*math.pi)*math.cos(float(earthquake.epi[0])/180*math.pi - float(lines_station[i].split(',')[1])/180*math.pi))
            #lines_station[i]=lines_station[i]+','+str(ang)
            ang_list.append(ang)
        station_num1=lines_station[ang_list.index(min(ang_list))].split(',')[0]
        targetstation=[station_num1]
        for i in range(1,num_of_station):
            ang_list[ang_list.index(min(ang_list))]=50
            station_num=lines_station[ang_list.index(min(ang_list))].split(',')[0]
            if (station_num=='StationNumber'):
                break
            targetstation.append(station_num)
        # print(targetstation)
        return targetstation
        g.close()
# earthquake=Earthquake()
# earthquake.initfrom('./cache/earthquake.csv',1)   
# ChooseDartStation(earthquake,100)

