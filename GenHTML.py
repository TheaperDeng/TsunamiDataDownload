#! /usr/bin/python
# -*- coding: utf-8 -*-

def GenHTML(filename,x,y,name):
    c=open(filename,"a")#<area shape="circle"coords="440,455,14"href ="P6.png"target ="_blank" />
    c.write(r'<area shape="circle"coords="')#DartData_32401PolynomialFit.png
    c.write(str(x)+','+str(y)+r',10"href ="')
    c.write(name+r'.png"target ="_blank" />')
    c.close()