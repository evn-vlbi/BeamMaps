#!/usr/bin/env python3

import sys
import numpy as np
import pylab
from datetime import datetime
from astropy.io import fits

#################
# Preliminaries #
#################

deg2rad=np.pi/180

#################
# Main          #
#################

if len(sys.argv) <3:
    print("\n Usage: %s log-file bbc_id\n" % sys.argv[0])
    print("  bbc_id, e.g. 1l, 1u, 2l ....\n")


# read log

try:
    f=open(sys.argv[1])
    fslog=f.readlines()
    f.close()
except:
    print("\n File \"%s\" not found\n" % sys.argv[1])
    sys.exit()

# Filter map x and y positions and total power counts

xl=np.array([])
yl=np.array([])
amp=np.array([])
tmpamp=[]
el=0
oldline=""
found=0
counts = {'1l':[]}
key='2l'
if len(sys.argv) ==3:
    key=sys.argv[2]

bbcl={'1l':"bbc01",'1u':"bbc01",'2l':"bbc02",'2u':"bbc02",'3l':"bbc03",'3u':"bbc03",'4l':"bbc04",'4u':"bbc04",'5l':"bbc05",'5u':"bbc05",'6l':"bbc06",'6u':"bbc06",'7l':"bbc07",'7u':"bbc07",'8l':"bbc08",'8u':"bbc08"}
bbcstr=bbcl[key]


for i in range(len(fslog)-1):
    if fslog[i][20:28]=="/source/":
        rest1,rest2,srcstr=fslog[i].split("/")
        source,ra,dec,epoch,rest,rest,rest,rest=srcstr.split(",")
        #print(source,ra,dec,epoch)
    if fslog[i][20:24]=="/lo/":
        rest1,rest2,lostr=fslog[i].split("/")
        lo1,lo2,sb1,sb2,pol1,pol2=lostr.split(",")
        #print(lo1,lo2,sb1,sb2,pol1,pol2)
    if fslog[i][21:26]==bbcstr:
        rest1,rest2,bbcstr=fslog[i].split("/")
        bfreq,IF,bw,rest,rest,rest,rest,rest,rest,rest,rest=bbcstr.split(",")
        #print(bfreq,IF,bw)
    if fslog[i][20:31]=="#holog#AzEl":
        rest,az,el=fslog[i].split()
        starttime=rest[:20]
        #print(starttime)
        #print(az,el)
    if fslog[i+1][20:31]=="#holog#Next":
        found=0
    if fslog[i][20:31]=="#holog#Next":
        #print("Next")
        rest,xoff,yoff=fslog[i].split()
        xl=np.append(xl,float(xoff))
        yl=np.append(yl,float(yoff))
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
        stoptime=fslog[i][:20]
        #print(stoptime)
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

x=np.unique(xl)
y=np.unique(yl)
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

# prepare for fits file
year=starttime[0:4]
daynum=starttime[5:8]
hr=starttime[9:11]
min=starttime[12:14]
sec=starttime[15:20]
# converting to date
res = datetime.strptime(year + "-" + daynum, "%Y-%j").strftime("%Y-%m-%d")
starttime=res + "T" + hr + ":" + min + ":" + sec

c1 = fits.Column(name='Azi', array=xl, format='E', unit='arcsec')
c2 = fits.Column(name='Elv', array=yl, format='E', unit='arcsec')
c3 = fits.Column(name='Counts', array=newamp, format='E')
t = fits.BinTableHDU.from_columns([c1, c2, c3])
t.header['EXTNAME'] = 'BEAMMAP'
t.header['DATE_OBS'] = starttime
t.header['OBJECT'] = source
t.header['FREQ'] = (float(lo1)+float(bfreq))
t.header['BANDWID'] = bw
t.writeto('beammap_'+key+'.fits',overwrite=True)

# resape for plotting

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

#pylab.show()
pylab.savefig('beammap_'+key+'.png')
# save as fits file (tbd)

