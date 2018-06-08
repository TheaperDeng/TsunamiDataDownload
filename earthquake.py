#! /usr/bin/python
# -*- coding: utf-8 -*-

import csv,re

class Earthquake():
    def __init__(self):
        self.date=['1970','01','01']
        self.time_zero=['00','00','30']
        self.magnitude=0
        self.depth=0
        self.epi=[0,0]#long,lati
        self.place=''
    def initfrom(self,filename,linenum):
        with open(filename) as f:
            reader=csv.reader(f)
            rows=[row for row in reader]
            row=rows[linenum]
            m=re.match(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})',row[0])
            if m:
                self.date=[m[1],m[2],m[3]]
                self.magnitude=float(row[4])
                self.depth=row[3]
                self.epi=[float(row[2]),float(row[1])]
                self.time_zero=[m[4],m[5],m[6]]
                self.place=row[13]
                #print(self.time_zero)
            else:
                pass
    def printall(self,filename):
        with open(filename) as f:
            reader=csv.reader(f)
            a=1
            for row in reader:
                m=re.match(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})',row[0])
                if m:
                    if a<10:
                        print(a,' :',"On",m[1],m[2],m[3],"at",m[4],':',m[5],":",m[6],"in",row[13])
                        a=a+1
                    else:
                        print(a,':',"On",m[1],m[2],m[3],"at",m[4],':',m[5],":",m[6],"in",row[13])
                        a=a+1   
                else:
                    pass
        
#earthquake=Earthquake()
#earthquake.initfrom('./cache/earthquake.csv',1)            