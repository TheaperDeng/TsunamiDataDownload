#! /usr/bin/python
# -*- coding: utf-8 -*-

class Settings():
    '''Setting class is a Input of all that filter condition of earthquakes'''
    def __init__(self):
        self.starttime='2011-03-03'#start at starttime
        self.endtime='2018-03-03'#end at endtime
        self.minmagnitude=7.5#only earthquakes which larger than 7.5 mag will be record
        self.maxdepth=50#only earthquakes which happened 50km or less will be record