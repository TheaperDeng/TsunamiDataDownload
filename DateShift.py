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
# newtime1=DateShift(['1970','02','28'],-1)#-1 means backward
# newtime2=DateShift(['1971','9','30'],1)#1 means forward
# print(newtime1)
# print(newtime2)
