#! /usr/bin/python
# -*- coding: utf-8 -*-
import datetime

def DateShift(date,shiftmode):
    Y=int(date[0])
    m=int(date[1])
    d=int(date[2])
    dayA=datetime.datetime(Y,m,d)
    dayB=dayA+datetime.timedelta(shiftmode)
    newdate=[dayA.year,dayB.month,dayB.day]
    return newdate
    
def Datedelta(y_1,m_1,d_1,y_2,m_2,d_2):
    time_1=datetime.datetime(y_1,m_1,d_1,22,23,14)
    time_2=datetime.datetime(y_2,m_2,d_2,22,23,12)
    print(time_1-time_2)
    
# Datedelta(2018,8,10,2018,8,11)
# newtime1=DateShift(['1970','02','28'],-1)#-1 means backward
# newtime2=DateShift(['1971','9','30'],1)#1 means forward
# print(newtime1)
# print(newtime2)
