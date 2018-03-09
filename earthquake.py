#! /usr/bin/python
# -*- coding: utf-8 -*-

import csv,re

class Earthquake():
    def __init__(self):
        self.date=['1970','01','01']
        self.time_zero=['00','00','30']
        self.magnitude=0
        self.depth=0
        self.epi=[0,0]
    def initfrom(self,filename,linenum):
        with open(filename) as f:
            reader=csv.reader(f)
            rows=[row for row in reader]
            row=rows[linenum]
            m=re.match(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})',row[0])
            if m:
                self.date=[m[1],m[2],m[3]]
                self.magnitude=float(row[4])
                self.depth=float(row[3])
                self.epi=[float(row[2]),float(row[1])]
                self.time_zero=[m[4],m[5],m[6]]
                print(self.time_zero)
            else:
                pass

earthquake=Earthquake()
earthquake.initfrom('./cache/earthquake.csv',1)            