#!/usr/bin/env python

import sys, string
import numpy as np
import pylab

#################
# Preliminaries #
#################

deg2rad=np.pi/180

#################
# Main          #
#################

# read log

try:
    f=open(sys.argv[1])
    fslog=f.readlines()
    f.close()
except:
    print "\n File \"%s\" not found\n" % sys.argv[1]
    sys.exit()


# Filter map x and y positions and total power counts

x=np.array([])
y=np.array([])
amp=np.array([])
tmpamp=[]
el=0
oldline=""
found=0
counts = {'1l':[]}
#key='2l'
key=sys.argv[2]
for i in range(len(fslog)-1):
    if fslog[i][20:31]=="#holog#AzEl":
        rest,az,el=fslog[i].split()
        #print(az,el)
    if fslog[i+1][20:31]=="#holog#Next":
        found=0
    if fslog[i][20:31]=="#holog#Next":
        #print("Next")
        rest,xoff,yoff=fslog[i].split()
        x=np.append(x,float(xoff))
        y=np.append(y,float(yoff))
	tmpamp=[]
	counts = {'1l':[]}
	found=1
    if fslog[i][20:34]=="#tpicd#tpcont/":
        newline=fslog[i].split('/')
        newline2=newline[1][:-1].split(',')
	oh=len(newline2) % 3
	stop=len(newline2)-oh
        for k in range(0,stop,3):
	    bbc=newline2[k]
	    ph1=float(newline2[k+1])
	    ph2=float(newline2[k+2])
	    #print(bbc,ph1,ph2)
	    try:
	        counts[bbc].append([ph1,ph2])
	    except KeyError:
	        counts[bbc]=[[ph1,ph2]]
	if found==0:
	    #print(counts[key])
	    #print(len(counts[key]))
	    for j in range(len(counts[key])):
		cal=counts[key][j][0]-counts[key][j][1]
		if cal> 0:
	            tA=(counts[key][j][0]+counts[key][j][1]-cal)/(2*cal)
		tmpamp.append(tA)
            amp=np.append(amp,np.average(tmpamp))
    if fslog[i][20:35]=="#holog#Finished":
	for j in range(len(counts[key])):
	    cal=counts[key][j][0]-counts[key][j][1]
	    if cal> 0:
	        tA=(counts[key][j][0]+counts[key][j][1]-cal)/(2*cal)
	    tmpamp.append(tA)
        amp=np.append(amp,np.average(tmpamp))
        #print("Finish")

#print(x)
#print(y)

# Prepare map

x=np.unique(x)
y=np.unique(y)
x=x*np.cos(float(el)*deg2rad)*3600
y=y*3600
#print(len(x),len(y),len(amp))

# resort amp for reverse scan direction
scandir=0
newamp=np.array([])
i=0
while i < len(amp):
    if i % len(x) ==0:
        scandir=scandir+1
        #print(i,len(x),len(amp))
    if scandir % 2 == 0:
        #print("even scansdir")
	for j in range(len(x),0,-1):
            newamp=np.append(newamp,amp[i+j-1])
	i=i+len(x)
    else:
        #print("odd scandir")
        newamp=np.append(newamp,amp[i])
        i=i+1

amp=newamp.reshape(len(y),len(x))
amp=np.log(amp)

# plot

fig=pylab.figure()

sub1=fig.add_subplot(111)
sub1.set_xlabel("Azi [arcsec]")
sub1.set_ylabel("Elv [arcsec]")

sub1.set_xlim(-1050,1050)
sub1.set_ylim(-1050,1050)
#pylab.title("Focused Beam")
#pylab.plot(x,y,'o')
pylab.contour(x,y,amp,16,colors='black')
pylab.contourf(x,y,amp,16)
#pylab.colorbar()
#legend
cbar = pylab.colorbar()
cbar.set_label("log($T_{sys}$) [counts]")

pylab.show()

# save as fits file (tbd)

