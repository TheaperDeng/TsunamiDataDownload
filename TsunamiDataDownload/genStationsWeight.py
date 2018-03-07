#! /usr/bin/python

import sys, re, math

stations = []
SpacePattern = re.compile('\s+')
f = open('Stations.ctl', 'r')
while True:
	s = f.readline()
	if len(s) == 0:
		break
	s = s.strip()
	if len(s) == 0:
		continue
	if s.startswith('#'):
		continue
	l = SpacePattern.split(s)
	stations.append(l[2])
f.close()

f = open('StationsWeight.ctl', 'w')
for i in range(0,len(stations)):
	f.write('1.0 '+stations[i]+'\n')
f.close()

