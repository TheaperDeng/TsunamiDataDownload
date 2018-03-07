#! /usr/bin/python

import urllib, urllib2, sys, re, math, os

def secondsSince20000101(time0):
	for i in range(0,len(time0)):
		time0[i]=int(time0[i])
	Year=time0[0]; Month=time0[1]; Day=time0[2];
	Days = 0
	for i in range(2000, Year):
		Days += 365
		if(((i%4==0)&(i%100!=0)) | (i%400==0)):
			Days += 1
	DaysInMonth=[31,28,31,30,31,30,31,31,30,31,30,31]
	if(((Year%4==0)&(Year%100!=0)) | (Year%400==0)):
		DaysInMonth[1] += 1
	for i in range(1,Month):
		Days += DaysInMonth[i-1]
	Days += Day-1
	return Days*24*3600+time0[3]*3600+time0[4]*60+time0[5]

def dateBasedOnSeconds(seconds):
	seconds = int(seconds)
	Year = 2000; Month = 1; Day = 1; Hour = 0; Minute = 0; Second = 0
	Days = seconds/86400; LeftSeconds = seconds-Days*86400
	while True:
		DaysInThisYear = 365
		if(((Year%4==0)&(Year%100!=0)) | (Year%400==0)):
			DaysInThisYear += 1
		if(Days < DaysInThisYear):
			break
		Days -= DaysInThisYear
		Year += 1
	DaysInMonth=[31,28,31,30,31,30,31,31,30,31,30,31]
	if(((Year%4==0)&(Year%100!=0)) | (Year%400==0)):
		DaysInMonth[1] += 1
	for i in range(0,len(DaysInMonth)):
		if(Days < DaysInMonth[i]):
			break
		Days -= DaysInMonth[i]
		Month += 1
	Day = Days+1
	Hour = LeftSeconds/3600
	Minute = (LeftSeconds-Hour*3600)/60
	Second = LeftSeconds-Hour*3600-Minute*60
	return [Year, Month, Day, Hour, Minute, Second]


def distanceAzimuthOnSphere(lat1, lon1, lat2, lon2):
	DegToRad = 3.14159265359/180.0
	phi1 = lat1*DegToRad; phi2 = lat2*DegToRad;
	theta1 = lon1*DegToRad; theta2=lon2*DegToRad;
	sind = math.sqrt((math.cos(theta1)*math.cos(phi1)-math.cos(theta2)*math.cos(phi2))**2 + \
	(math.sin(theta1)*math.cos(phi1)-math.sin(theta2)*math.cos(phi2))**2 + \
	(math.sin(phi1)-math.sin(phi2))**2) * \
	math.sqrt((math.cos(theta1)*math.cos(phi1)+math.cos(theta2)*math.cos(phi2))**2 + \
	(math.sin(theta1)*math.cos(phi1)+math.sin(theta2)*math.cos(phi2))**2 + \
	(math.sin(phi1)+math.sin(phi2))**2) * 0.5
	cosd = math.sin(phi1)*math.sin(phi2)+math.cos(phi1)*math.cos(phi2)*math.cos(theta1-theta2)
	dis = math.atan2(sind, cosd)/DegToRad
	az = math.atan2((math.cos(phi2)*math.sin(theta2-theta1))/sind, \
	(math.sin(phi2)-math.sin(phi1)*cosd)/math.cos(phi1)/sind)/DegToRad
	if(az < 0.0):
		az = az + 360.0
	baz = math.atan2(math.cos(phi1)*math.sin(theta2-theta1)/sind, \
	(math.sin(phi1)-math.sin(phi2)*cosd)/math.cos(phi2)/sind)/DegToRad
	baz = 360.0 - baz
	if(baz >= 360.0):
		baz = baz - 360.0
	return [dis, az, baz]


stations = []

StartTime = ['2010', '4', '6']
EndTime = ['2010', '4', '7']
time0 = [2010,4,6,22,15,01]
Epi = [97.048, 2.383] # lon, lat


EarthquakeFromCatalog = -1
if(len(sys.argv) == 2):
	EarthquakeFromCatalog = int(sys.argv[1])
MaxStationsNum = 5

SortStationsByDistance = True


if(EarthquakeFromCatalog >= 1):
	num = 0; Mw = []; depth = []; name = []; time = []; lat = []; lon = []
	f = open('EarthquakeCatalog.csv', 'r')
	f.readline()
	while True:
		s = f.readline()
		if(len(s) == 0):
			break
		s = s.strip()
		if(len(s) == 0):
			continue
		num = num+1
		l = s.strip().split(',')
		Mw.append(l[4])
		depth.append(l[3])
		name.append(s.split('"')[1].strip())
		ll = l[0].replace('T','-').replace('Z','').replace(':','-').split('-')
		ll[len(ll)-1]=str(int(float(ll[len(ll)-1])))
		time.append(ll)
		lat.append(l[1])
		lon.append(l[2])
	f.close()
	if(EarthquakeFromCatalog > num):
		EarthquakeFromCatalog = num
	
	i = EarthquakeFromCatalog
	print('\nTotal '+str(num)+' events, using Event # '+str(i)+':\n')

	i = i-1
	print(name[i])
	print('Mw '+Mw[i]+', depth '+depth[i]+', time '+'-'.join(time[i])+'\n')

	StartTime = time[i][0:3]
	EndTime = time[i][0:3]
	if(int(time[i][3]) < 6):
		NewStartTime = dateBasedOnSeconds(secondsSince20000101(time[i])-6*60*60)
		StartTime[0:3] = [str(x) for x in NewStartTime[0:3]]
	elif(int(time[i][3]) >= 18):
		NewEndTime = dateBasedOnSeconds(secondsSince20000101(time[i])+6*60*60)
		EndTime[0:3] = [str(x) for x in NewEndTime[0:3]]
	time0 = time[i]
	Epi = [float(lon[i]), float(lat[i])]



sta = []; lat = []; lon = []; wd = []
SpacePattern = re.compile('\s+')
f = open('DARTStationsInfo.info', 'r')
while True:
	s = f.readline()
	if(len(s) == 0):
		break
	lst = SpacePattern.split(s.strip())
	IsAppend = False
	if(len(stations) == 0):
		IsAppend = True
	else:
		for ista in range(0,len(stations)):
			if(stations[ista].lower() == lst[0]):
				IsAppend = True
				break
	if IsAppend:
		sta.append(lst[0])
		lon.append(float(lst[1]))
		lat.append(float(lst[2]))
		wd.append(float(lst[3]))
f.close()
stations = sta

if SortStationsByDistance:
	dist = []
	for IS in range(0,len(stations)):
		[ThisDist, az, baz] = distanceAzimuthOnSphere(Epi[1], Epi[0], lat[IS], lon[IS])
		dist.append(ThisDist)
	for IS in range(0, len(stations)-1):
		for JS in range(IS+1, len(stations)):
			if(dist[IS] > dist[JS]):
				s = stations[IS]; stations[IS] = stations[JS]; stations[JS] = s
				s = dist[IS]; dist[IS] = dist[JS]; dist[JS] = s
				s = lon[IS]; lon[IS] = lon[JS]; lon[JS] = s
				s = lat[IS]; lat[IS] = lat[JS]; lat[JS] = s
				s = wd[IS];  wd[IS] = wd[JS];   wd[JS] = s

if(MaxStationsNum >= 1):
	stations = stations[0:MaxStationsNum]


StationsGood = []
StartStr = "#yy  mm dd hh mm ss t   height"
EndStr = "</textarea></label></pre>"
t0 = secondsSince20000101(time0)

for IS in range(0,len(stations)):
	DataFileName = stations[IS]+'.txt'
	try:
		os.remove(DataFileName)
	except OSError:
		pass
	DataFileName = stations[IS]+'.dat'
	try:
		os.remove(DataFileName)
	except OSError:
		pass

for IS in range(0,len(stations)):
	station = stations[IS]
	sys.stdout.write('Station '+station+':    ')

	urlNOAADart = "http://www.ndbc.noaa.gov/station_page.php?station=" + station + "&type=0&startyear=" + StartTime[0] + "&startmonth=" + StartTime[1] + "&startday=" + StartTime[2] + "&endyear=" + EndTime[0] + "&endmonth=" + EndTime[1] + "&endday=" + EndTime[2] + "&submit=Submit"

	req = urllib2.Request(urlNOAADart)
	response = urllib2.urlopen(req)
	the_page = response.read().lower()

	if(the_page.find(StartStr) == -1):
		sys.stdout.write('NO DATA\n')
	else:
		s = re.compile('<b>\d+\.\d+\s+[ns]\s+\d+\.\d+\s+[ew]').findall(the_page)[0].replace('<b>','')
		s = StartStr +  the_page.split(StartStr)[1].split(EndStr)[0]
		l = s.split('\n')
		IsEmpty = True
		for i in range(2,len(l)):
			ss = l[i].strip()
			if((len(ss) > 0) and (ss.endswith('9999.000') == False)):
				IsEmpty = False; break
		if(IsEmpty == True):
			sys.stdout.write('NO DATA\n')
		else:
			SourceFileName = stations[IS]+'.txt'
			f = open(SourceFileName,'w')
			f.write(s)
			f.close()

			SourceFile = open(SourceFileName,'r')
			time = []; data = []
			while True:
				s = SourceFile.readline()
				if len(s) == 0:
					break
				s = s.strip()
				if len(s) == 0:
					continue
				if s.startswith('#'):
					continue
				l = SpacePattern.split(s)
				time1 = l[0:6]
				t1 = secondsSince20000101(time1)
				data1 = float(l[7])
				if(math.fabs(data1) > 9000.0):
					continue
				if(len(time)>0) and (t1-t0) == time[len(time)-1]:
					continue
				if(len(data)>0 and math.fabs(data1-data[len(data)-1]) > 10.0):
					continue
				time.insert(len(time),t1-t0)
				data.insert(len(data),data1)
			SourceFile.close()
			DataFileName = stations[IS]+'.txt'
			DataFile = open(DataFileName,'w')
			for i in range(len(time)-1,-1,-1):
				DataFile.write(str(time[i]).ljust(15,' ')+str(data[i])+'\n')
			DataFile.close()

			sys.stdout.write('done\n')
			StationsGood.append(IS)

f = open('Stations.ctl','w')
for i in range(0,len(StationsGood)):
	IS = StationsGood[i]
	f.write(str(lon[IS])+' '+str(lat[IS])+' '+stations[IS])
	if(i != len(StationsGood)-1):
		f.write('\n')
f.close()

f = open('StationsLocationDART.gmttxt','w')
f.write('Longitude Lattiude\n')
for i in range(0,len(StationsGood)):
	IS = StationsGood[i]
	f.write(str(lon[IS])+'\t'+str(lat[IS])+'\t'+stations[IS])
	if(i != len(StationsGood)-1):
		f.write('\n')
f.close()

f = open('StationsNamesDART.gmttxt','w')
for i in range(0,len(StationsGood)):
	IS = StationsGood[i]
	f.write(str(lon[IS])+'\t'+str(lat[IS])+'\t'+'20'+'\t'+'0'+'\t'+'0'+'\tTC'+'\t'+stations[IS])
	if(i != len(StationsGood)-1):
		f.write('\n')
f.close()


f = open('EpiLocation.gmttxt', 'w')
f.write('Longitude Latitude\n'+str(Epi[0])+' '+str(Epi[1]))
f.close()
