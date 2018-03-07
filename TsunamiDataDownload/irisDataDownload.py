#! /usr/bin/python
# Created by Chao An (ca298@cornell.edu)
# Downloaded mseed/RESP/SAC_PZs from IRIS, convert mseed to SACs
# iris service: http://service.iris.edu/

# input: irisDataDownload.ctl, rdseed (from iris), BUD_2013.280.541912.dataless

import urllib, urllib2, sys, math, time, os, subprocess, shutil, re


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

def downloadData(StationsNet, StationsName, AllParams):
	[EventName, EpiTime, EpiLocation, StartTime, EndTime, MinDist, MaxDist, RealTimeOnly, RemoveUnpairedSAC] = AllParams
	serverURL0 = 'http://service.iris.edu/fdsnws/dataselect/1/'
	serverURL = serverURL0 + 'query?nodata=404&loc=00&cha=BH?&'
	episec = secondsSince20000101(EpiTime)
	StartDate = dateBasedOnSeconds(episec+StartTime)
	EndDate =  dateBasedOnSeconds(episec+EndTime)
	JulyDay = (secondsSince20000101(StartDate)-secondsSince20000101([StartDate[0],1,1,StartDate[3],StartDate[4],StartDate[5]]))/86400+1
	for i in range(0,len(StartDate)):
		StartDate[i] = str(StartDate[i])
		if(i != 0):
			StartDate[i] = StartDate[i].rjust(2,'0')
		EndDate[i] = str(EndDate[i])
		if(i != 0):
			EndDate[i] = EndDate[i].rjust(2,'0')
	serverURL += 'start='+StartDate[0]+'-'+StartDate[1]+'-'+StartDate[2]+'T'+StartDate[3]+':'+StartDate[4]+':'+StartDate[5]+'.000'
	serverURL += '&end='+EndDate[0]+'-'+EndDate[1]+'-'+EndDate[2]+'T'+EndDate[3]+':'+EndDate[4]+':'+EndDate[5]+'.000'
	NetWorks = ''; Stations = '';
	for i in range(0, len(StationsNet)):
		NetWorks += StationsNet[i]
		Stations += StationsName[i]
		if(i != len(StationsNet)-1):
			NetWorks += ','; Stations += ','
	MSeedURL = serverURL + '&net='+NetWorks+'&sta='+Stations
	MSeedDataFileName = str(StartDate[0])+'_'+str(JulyDay).rjust(3,'0')+'_'+StartDate[3]+'_'+StartDate[4]+'_'+StartDate[5]+\
	     '_Duration'+str(EndTime-StartTime)+'.mseed'
	print '    write into '+MSeedDataFileName
	try:
		MSeed = urllib2.urlopen(MSeedURL)
		MSeedDataFile = open(MSeedDataFileName,'wb')
		ChunkSize = 500000; BytesSoFar = 0; PrintNum = 0;
		while True:
			if(PrintNum%5 == 0):
				sys.stdout.write('\n    '+str(BytesSoFar/1000.0).rjust(6,' ')+'K'); sys.stdout.flush()
			chunk = MSeed.read(ChunkSize)
			if not chunk:
				break
			BytesSoFar += len(chunk)
			MSeedDataFile.write(chunk)
			sys.stdout.write('======>'+str(BytesSoFar/1000.0).rjust(6,' ')+'K'); sys.stdout.flush()
			PrintNum += 1
		MSeedDataFile.close()
		print '\n\n    Data dowloading finished. Data size = '+str('%0.2f'%(BytesSoFar/1000.0/1000.0))+'M.'
		return MSeedDataFileName
	except urllib2.URLError, e:
		print '    Error downloading data ...'
		print e
		print
		exit(0)

def downloadRESP(StationsNet, StationsName, AllParams):
	[EventName, EpiTime, EpiLocation, StartTime, EndTime, MinDist, MaxDist, RealTimeOnly, RemoveUnpairedSAC] = AllParams
	ResponseURL0 = 'http://service.iris.edu/irisws/resp/1/'
	ResponseURL = ResponseURL0 + 'query?loc=00&'
	
	episec = secondsSince20000101(EpiTime)
	StartDate = dateBasedOnSeconds(episec+StartTime)
	EndDate =  dateBasedOnSeconds(episec+EndTime)
	JulyDay = (secondsSince20000101(StartDate)-secondsSince20000101([StartDate[0],1,1,StartDate[3],StartDate[4],StartDate[5]]))/86400+1
	for i in range(0,len(StartDate)):
		StartDate[i] = str(StartDate[i])
		if(i != 0):
			StartDate[i] = StartDate[i].rjust(2,'0')
		EndDate[i] = str(EndDate[i])
		if(i != 0):
			EndDate[i] = EndDate[i].rjust(2,'0')
	ResponseURL += 'start='+StartDate[0]+'-'+StartDate[1]+'-'+StartDate[2]+'T'+StartDate[3]+':'+StartDate[4]+':'+StartDate[5]+'.000'
	ResponseURL += '&end='+EndDate[0]+'-'+EndDate[1]+'-'+EndDate[2]+'T'+EndDate[3]+':'+EndDate[4]+':'+EndDate[5]+'.000'
	for i in range(0, len(StationsNet)):
		if((i+1)%10 == 0):
			print '    '+str(i+1)+'  of  '+str(len(StationsNet))
		ThisURL = ResponseURL + '&net='+StationsNet[i]+'&sta='+StationsName[i]
		ChannelList = ['1','2','N','E','Z']
		for j in range(0, len(ChannelList)):
			try:
				Response = urllib2.urlopen(ThisURL+'&cha=BH'+ChannelList[j])
				ResponseFileName = Response.info().getheaders("Content-Disposition")[0].split('filename=')[1]
				ResponseFile = open(ResponseFileName,'w')
				ResponseFile.write(Response.read())
				ResponseFile.close()
			except urllib2.URLError, e:
				x = 1
				#print 'Error downloading RESP: '+StationsNet[i]+'.'+StationsName[i]+': '+'BH'+ChannelList[j]
	print '\nInstrument response dowloading finished.\n'


def downloadSAC_PZs(StationsNet, StationsName, AllParams):
	[EventName, EpiTime, EpiLocation, StartTime, EndTime, MinDist, MaxDist, RealTimeOnly, RemoveUnpairedSAC] = AllParams
	pzsURL0 = 'http://service.iris.edu/irisws/sacpz/1/'
	pzsURL = pzsURL0 + 'query?loc=00&'
	
	episec = secondsSince20000101(EpiTime)
	StartDate = dateBasedOnSeconds(episec+StartTime)
	EndDate =  dateBasedOnSeconds(episec+EndTime)
	JulyDay = (secondsSince20000101(StartDate)-secondsSince20000101([StartDate[0],1,1,StartDate[3],StartDate[4],StartDate[5]]))/86400+1
	for i in range(0,len(StartDate)):
		StartDate[i] = str(StartDate[i])
		if(i != 0):
			StartDate[i] = StartDate[i].rjust(2,'0')
		EndDate[i] = str(EndDate[i])
		if(i != 0):
			EndDate[i] = EndDate[i].rjust(2,'0')
	pzsURL += 'start='+StartDate[0]+'-'+StartDate[1]+'-'+StartDate[2]+'T'+StartDate[3]+':'+StartDate[4]+':'+StartDate[5]+'.000'
	pzsURL += '&end='+EndDate[0]+'-'+EndDate[1]+'-'+EndDate[2]+'T'+EndDate[3]+':'+EndDate[4]+':'+EndDate[5]+'.000'
	for i in range(0, len(StationsNet)):
		if((i+1)%10 == 0):
			print '    '+str(i+1)+'  of  '+str(len(StationsNet))
		ThisURL = pzsURL + '&net='+StationsNet[i]+'&sta='+StationsName[i]
		ChannelList = ['1','2','N','E','Z']
		for j in range(0, len(ChannelList)):
			try:
				pzs = urllib2.urlopen(ThisURL+'&cha=BH'+ChannelList[j])
				pzsFileName = pzs.info().getheaders("Content-Disposition")[0].split('filename=')[1]
				pzsFile = open(pzsFileName,'w')
				pzsFile.write(pzs.read())
				pzsFile.close()
			except urllib2.URLError, e:
				x = 1
				#print 'Error downloading SAC PZs: '+StationsNet[i]+'.'+StationsName[i]+': '+'BH'+ChannelList[j]
	print '\nSAC PZs dowloading finished.\n'


def getStationsInfo(AllParams):
	[EventName, EpiTime, EpiLocation, StartTime, EndTime, MinDist, MaxDist, RealTimeOnly, RemoveUnpairedSAC] = AllParams
	episec = secondsSince20000101(EpiTime)
	stainfoURL = 'http://www.iris.edu/cgi-bin/xmlstationinfo/'
	ThisURL = stainfoURL+'_GSN';
	req = urllib2.Request(ThisURL)
	response = urllib2.urlopen(req)
	the_page = response.read().lower()
	l = the_page.split('/>')
	StationsNet = []; StationsName = []; StationsLat = []; StationsLon = []; nStations = 0;
	for i in range(0,len(l)):
		if(l[i].find('station net=') == -1):
			continue
		if(l[i].split('rtdata=')[1].split('"')[1].find('realtime') != -1):
			if(RealTimeOnly == 1):
				continue
		ardata = l[i].split('ardata="')[1].split('"')[0].split('-')
		ls = [int(x) for x in ardata[0].strip().split('/')]
		le = [int(x) for x in ardata[1].strip().split('/')]
		if((secondsSince20000101(ls+[0,0,0]) >= episec+StartTime) or (secondsSince20000101(le+[0,0,0]) <= episec+EndTime)):
			continue
		stalat = float(l[i].split('lat="')[1].split('"')[0])
		stalon = float(l[i].split('lon="')[1].split('"')[0])
		[d, az, baz] = distanceAzimuthOnSphere(EpiLocation[0], EpiLocation[1], stalat, stalon)
		if((d < MinDist) or (d > MaxDist)):
			continue
		StationsNet.append(l[i].split('station net="')[1].split('"')[0].upper())
		StationsName.append(l[i].split('sta="')[1].split('"')[0].upper())
		StationsLat.append(float(l[i].split('lat="')[1].split('"')[0]))
		StationsLon.append(float(l[i].split('lon="')[1].split('"')[0]))
		nStations = nStations+1
	print '    Use '+str(nStations)+' stations'
	f = open('AllStationsInfo.txt','w')
	for i in range(0,len(StationsNet)):
		f.write(StationsNet[i].ljust(2,' ')+' '+StationsName[i].ljust(4,' ')+' '\
		    +str(StationsLat[i]).rjust(8,' ')+' '+str(StationsLon[i]).rjust(8,' ')+'\n')
	f.close()
	return [nStations, StationsNet, StationsName, StationsLat, StationsLon]


def readParameters():
	f = open('irisDataDownload.ctl','r')
	while True:
		s = f.readline()
		if(len(s) == 0):
			break
		s = s.strip()
		if((len(s) == 0) or (s[0] == '#')):
			continue
		slower = s.lower()
		if(slower[0:49].find('Event Name'.lower()) != -1):
			EventName = s[49:].strip().split('#')[0].strip()
		elif(slower[0:49].find("Earthquake time".lower()) != -1):
			EpiTime = [int(x) for x in s[49:].strip().split('#')[0].strip().split(',')]
		elif(slower[0:49].find("Epicenter location".lower()) != -1):
			EpiLocation = [float(x) for x in s[49:].strip().split('#')[0].strip().split(',')]
		elif(slower[0:49].find("Data starting/ending time from earthquake".lower()) != -1):
			l = [float(x) for x in s[49:].strip().split('#')[0].strip().split(',')]
			StartTime = l[0]*60; EndTime = l[1]*60;
		elif(slower[0:49].find("Stations min/max distance".lower()) != -1):
			l = [float(x) for x in s[49:].strip().split('#')[0].strip().split(',')]
			MinDist = l[0]; MaxDist = l[1];
		elif(slower[0:49].find("Stations with realtime data ONLY".lower()) != -1):
			RealTimeOnly = int(s[49:].strip().split('#')[0])
		elif(slower[0:49].find("Remove unpaired SACs".lower()) != -1):
			RemoveUnpairedSAC = int(s[49:].strip().split('#')[0])
	f.close()
	return [EventName, EpiTime, EpiLocation, StartTime, EndTime, MinDist, MaxDist, RealTimeOnly, RemoveUnpairedSAC]
	
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


print '\nRead config...'
AllParams = readParameters()
[EventName, EpiTime, EpiLocation, StartTime, EndTime, MinDist, MaxDist, RealTimeOnly, RemoveUnpairedSAC] = AllParams
# StartTime, EndTime in seconds

msg = '\nGetting GSN stations info...'
if(RealTimeOnly == 1):
	msg += " real time data only..."
print msg
[nStations, StationsNet, StationsName, StationsLat, StationsLon] = getStationsInfo(AllParams)

print '\nDownloading data ...'
downloadData(StationsNet, StationsName, AllParams)

#print '\nDownloading RESP...'
#downloadRESP(StationsNet, StationsName, AllParams)

print '\nDownloading SAC PZs...'
downloadSAC_PZs(StationsNet, StationsName, AllParams)

print '\nConvert mseed to SAC...'
if(os.path.isfile('rdseed.err_log')):
	os.remove('rdseed.err_log')
for f in os.listdir('.'):
	if(f.endswith('mseed')):
		MSeedDataFileName = f
		break
icmd = ['rdseed', '-f', MSeedDataFileName, '-g', 'BUD_2013.280.541912.dataless', '-i', '-d', '-o', '1'];
#-f: input file name(miniseed); -g: dataless seed file; -i: ignore location code; -d: output data; -o: output data format
try:
	p = subprocess.Popen(icmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	ConvertLog = p.communicate()[1]
except OSError, e:
	print e
print'\nEND\n'

