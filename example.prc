define  hologi       00000000000x
log=beammap
"astro16
" take 8 MHz at 21cm, because of RFI
astro8
!+30s
" Some additional information for the FITS header
" Which source and frequency is used
source
lo
bread
sy=go holog &
enddef
define  hologp       00000000000x
data_valid=on
!+20s
data_valid=off
sy=go holog &
enddef
define  astro16       00000000000x
pcaloff
tpicd=stop
"vsi-12 input should be used in 'equip.ctl'
"... vsi1 is also supported
"... vsi2 is supported if firmware is v105 or later
fila10g_mode=,0xffffffff,,32.000
fila10g_mode
mk5c_mode=vdif,0xffffffff,,32.00
mk5c_mode
form=astro
form
bbc01=100.49,a,16.00
bbc02=132.49,a,16.00
bbc03=164.49,a,16.00
bbc04=196.49,a,16.00
bbc05=100.49,b,16.00
bbc06=132.49,b,16.00
bbc07=164.49,b,16.00
bbc08=196.49,b,16.00
ifd01
cont_cal=on,2,4
bbc_gain=all,agc,12000
tpicd=no,200
tpicd
enddef
define  ifd01         00000000000
ifa=1,agc,2,48000
ifb=3,agc,2,48000
lo=loa,1230.00,usb,rcp,off
lo=lob,1230.00,usb,lcp,off
enddef
define  astro8       000000000000
pcaloff
tpicd=stop
"vsi-12 input should be used in 'equip.ctl'
"... vsi1 is also supported
"... vsi2 is supported if firmware is v105 or later
fila10g_mode=,0xffffffff,,16.000
fila10g_mode
mk5c_mode=vdif,0xffffffff,,16.00
mk5c_mode
form=astro
form
bbc01=124.49,a,8.00
bbc02=140.49,a,8.00
bbc03=156.49,a,8.00
bbc04=172.49,a,8.00
bbc05=124.49,b,8.00
bbc06=140.49,b,8.00
bbc07=156.49,b,8.00
bbc08=172.49,b,8.00
ifd01
cont_cal=on,2,4
bbc_gain=all,agc,12000
tpicd=no,400
tpicd
enddef
