#! /usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.messagebox as messagebox
from settings import Settings
from GetUsgsData import GetUsgsData,GetUrlFromSettings
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master,height = 2000,width = 4000)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        e = StringVar()    
        e.set('starttime e.g.2018-03-06')  
        self.starttime = Entry(self,textvariable=e)
        self.starttime.pack()
        g = StringVar()
        g.set('endtime e.g.2018-03-06')  
        self.endtime = Entry(self,textvariable=g)
        self.endtime.pack()
        h = StringVar()
        h.set('minmagnitude e.g.7.5')  
        self.minmagnitude =Entry(self,textvariable=h)
        self.minmagnitude.pack()
        j = StringVar()
        j.set('maxdepth(km) e.g.50')  
        self.maxdepth= Entry(self,textvariable=j)
        self.maxdepth.pack()
        self.alertButton = Button(self, text='Get!', command=self.hello)
        self.alertButton.pack()
    def hello(self):
        Earthquake_Settings=Settings() 
        starttime = self.starttime.get() or '2011-03-06'
        endtime = self.endtime.get() or '2018-03-06'
        minmagnitude = self.minmagnitude.get() or 7.5
        maxdepth = self.maxdepth.get() or 50
        Earthquake_Settings.starttime=starttime
        Earthquake_Settings.endtime=endtime
        Earthquake_Settings.minmagnitude=minmagnitude
        Earthquake_Settings.maxdepth=maxdepth
        GetUsgsData(Earthquake_Settings)

app = Application()
app.master.title('Hello World')
app.mainloop()
