# BeamMaps
Script and example procedure to measure radio antenna beam maps with the VLBI Field System. It should work, but it is likely only a first draft and needs to be updated with more experience from different stations.

The example procedure file contains the required commands to run the `holog` program.

To image the primary beam pattern a map size of about 4-5 beams should be sufficent. `holog` performs a raster map. To sample the map properly the separation between each raster point should be about 1/2.75 of the full width half maximum (FWHM) of the beam. The Effelsberg example was performed with 11 points on 4 beams.

The following steps are needed to perform a map. 

1. Find a brigth and point like source around the south or northern collimation (less changes in elevation when the source collimates.). 
2. Use the FS to point to the source
3. Load the corresponding receiver setup
4. Configure the `holog` parameters (see help below)
4. Start the `holog` program

`holog` will run two procedures which are named during the process of configuring `holog`. There is an intial procedure that is called only once at the start (procedure base name + i) and a procedure that is called for every raster point (procedure base name + p). In the example the procedure base name is just *holog* and the corresponding procedure in the station.prc of the FS are *hologi* and *hologp*.

### Example

The FWHM of the Effelsberg beam at 1.4 GHz is about 0.155 deg. A four beams wide map with 11x11 raster points would then be

`holog=0.62,0.62,11,11,,holog,`

with 

```
holog=azs,els,azp,elp,recal,proc,wait
	
Settable parameters:
	azs       Azimuth   Span: -360. to +360, non-inclusive. No default.
	els       Elevation Span:  -90. to  +90, non-inclusive. No default.
	azp       Azimuth Points: positive or negative odd values 1-99.
	          Magnitude of one does a single cut in elevation.
	          Negative values cause the "furrows" to be in
	          elevation. See comments. No default.
	elp       Elevation Points: positive or negative odd values 1-99.
	          Magnitude of one does a single cut in azimuth.
	          Negative values turn off the secant(elevation)
	          correction for azimuth.  No default.
	recal     Re-calibration period. Seconds: 0-10000 or "off".
	          0="off", Default is "off".
	proc      Snap procedure base name. See comments. No default.
	wait      Seconds to wait for onsource for each point, 1-1000
	          seconds allowed, default 120.
```

For a more detailed explanation with comments and examples type `help=holog` in the FS or the holog_help.txt above.

*recal* and *wait* are set to default, the *proc* is called holog. In the example.prc file the *hologi* procedure sets the corresponding settings for the DBBC2 VLBI backend and provides the channel selection for the TPICD measurements in the *hologp* procedure. The log-file is set to beammap.log

Once this is set, the program is start with

`holog`

This will run for some time. If each raster point takes about 30s it will last 11x11x30s=2640s. About 45min.

The measurement stops with the message *#holog#Finished*

Finally, the log-file can be processed with 

`fs_beammap.py <log-file> <bbc ID>`

e.g.

`fs_beammap.py beammap.log 8u`

It will produce a FITS file containing the map data in a table and an image file.

The python script should run with both python2 and 3. It requires numpy, astropy, and pylab.

## Possible improvements

I'm sure there are better ways to perform some of the processing in the python script. The FITS file might need some more auxilary information to be useful.

Ed Himwich suggested

1. use tpicd=yes,200 and then tpicd/tpicd=stop to start stop Tsys recording, then it is not dependent on data_valid, which has a specific meaning.
2. It seemed like there was a long delay in hologi that may not be needed.
3. "recalibration" points might be useful for removing changes in Tsys with elevation.
4. You might consider turning AGC off and using TPI.

I haven't tried it yet. 
