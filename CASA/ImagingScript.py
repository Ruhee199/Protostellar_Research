# The following measurement set is the result from the calibration script.
vislist=['uid___A002_X99c183_X25b6.ms.split.cal']
finalvis='uid___A002_X99c183_X25b6.ms.split.cal.source'
contvis='calibrated_final_cont.ms'
contspws='2,5'

#Identify Spectral Lines
plotms(vis=finalvis, xaxis='channel', yaxis='amplitude',
   	ydatacolumn='data',
   	avgtime='1e8', avgscan=True, avgchannel='1',
   	iteraxis='spw' )

#Dirty image of tclean
testimagename=’testImage’
field=['0'] #list all target fields
spw=['0','1','3','4'] #list all target spw’s

for i in field:
      for j in spw:  
            tclean(vis=finalvis,
            	  imagename=testimagename+'Field_'+str(i)+'_spw_'+str(j), 
            	  field=str(i),
      	          spw=str(j),
                  #phasecenter=phasecenter, 
# uncomment if mosaic and set to appropriate field number
		  #phasecenter='TRACKFIELD' 
# uncomment if imaging an ephemeris object, the phasecenter needs to be TRACKFIELD, not a field number as above.
		  specmode='cube',
                  veltype=veltype,
                  nchan=-1,
      	          outframe='REST', 
      	          niter=0,
      	          interactive=True,
      	          cell=cell,
      	          imsize=imsize, 
      	          weighting=weighting, 
      	          robust=robust,
		  pbcor=True,
                  restoringbeam='common',
      	          gridder=gridder)

#Saving version
flagmanager(vis=finalvis,mode='save',
versionname='before_cont_flags')

#Weights of channel
initweights(vis=finalvis,wtmode='weight',dowtsp=True)



#Spectral Window
flagchannels='0:740~840,1:720~880,3:550~1250,4:860~920' # modify the channel range for your dataset

flagdata(vis=finalvis,mode='manual',
      	spw=flagchannels,flagbackup=False)

# check that flags are as expected, NOTE must check reload on plotms
# gui if its still open.
plotms(vis=finalvis,yaxis='amp',xaxis='channel',
   	avgchannel='1',avgtime='1e8',avgscan=True,iteraxis='spw')
#The above code HAS NOT been run or tested
################################################################

#Selects all fields for Mosaic
field='5~18'
phasecenter=10
gridder='mosaic'
cell='0.20arcsec'
imsize = [450,450]
outframe='lsrk' # velocity reference frame. See science goals.
veltype='radio' # velocity type.
weighting = 'briggs'
robust=1
niter=10000
threshold = '0.0mJy'




#Running tclean

contvis = 'calibrated_final_cont.ms'         
contimagename = 'BHR71_cont'

tclean(vis=contvis,
       imagename=contimagename,
       field=field,
       phasecenter=phasecenter, # uncomment if mosaic or imaging an ephemeris object
       mosweight=True, # uncomment if mosaic     
       specmode='mfs',
       deconvolver='hogbom', 
       # Uncomment the below to image with nterms>1. Use if fractional bandwidth is >10%.
       #deconvolver='mtmfs',
       #nterms=2,
       imsize = imsize, 
       cell= cell, 
       weighting = weighting,
       robust = robust,
       niter = niter, #include multiscale cleaning
       threshold = threshold,
       interactive = True,
       gridder = gridder,
       pbcor = True,
       usepointing=False)

#################################################################

#UV Subtraction

##################################################################

rmtables(finalvis+'.contsub')
fitspw = '0:0~740;840~1919,1:0~720;880~1919,3:0~550;1250~1919,4:0~860;921~1919'
uvcontsub(vis=finalvis,
          field='1~18', #5~18, ran with 1~18 tho
          spw='0,1,3,4',
          fitspw=fitspw,
          combine='spw', #combine='spw,scan'
          solint='int',
          fitorder=1,
          want_cont=False)

listobs('uid___A002_X99c183_X25b6.ms.split.cal.source.contsub',
        listfile='uid___A002_X99c183_X25b6.ms.split.cal.source.contsub.listobs')

#################################################################

#Line Imaging

##################################################################

finalvis ='uid___A002_X99c183_X25b6.ms.split.cal.source'


# uncomment if you have neither continuum subtracted nor self-calibrated your data
# linevis = finalvis
# uncomment if you have continuum subtracted your data
linevis = finalvis + '.contsub'
# uncomment if you have both continuum subtracted and self-calibrated your data
# linevis = finalvis + '.contsub.selfcal'
# uncomment if you have only self-calibrated your data
# linevis = finalvis + '.selfcal'

#Setting Parameters for c18o
sourcename ='BHR71' # name of source
linename = 'c18o' # name of transition 
lineimagename = sourcename+'_'+linename # name of line image
spw = '0' # update to the spw you would like to image
restfreq='219.56036GHz'
start = '-8.6km/s'
width = '0.084km/s'
nchan = 100
outframe='lsrk' # velocity reference frame. See science goals.
veltype='radio' # velocity type.

#These were parameters set above
#field='1~14'
field='4~17' #look before putting into CASA
phasecenter=13 #check again before implement 
gridder='mosaic'
cell='0.20arcsec'
imsize = [450,450]
outframe='lsrk' # velocity reference frame. See science goals.
veltype='radio' # velocity type.
weighting = 'briggs'
robust=1 #0.5 (see if beam size changes, S/N not sacrificed)
niter=10000
threshold = '0.0mJy'



# Cleaning c18o

tclean(vis=linevis,
       imagename=lineimagename, 
       field=field,
       spw=spw,
       phasecenter=phasecenter, # uncomment if mosaic or imaging an ephemeris object   
       mosweight = True, # uncomment if mosaic      
       specmode='cube', # comment this if observing an ephemeris source
       #specmode='cubesource', #uncomment this line if observing an ephemeris source
       perchanweightdensity=False, # uncomment if you are running in CASA >=5.5.0
       start=start,
       width=width,
       nchan=nchan, 
       outframe=outframe,
       veltype=veltype, 
       restfreq=restfreq, 
       niter=niter,  
       threshold=threshold, 
       interactive=True,
       cell=cell,
       imsize=imsize, 
       weighting=weighting,
       robust=robust,
       gridder=gridder,
       deconvolver='multiscale',
       scales=[0,5,15,20,25],
       usemask='auto-multithresh',
       sidelobethreshold=2.0,
       noisethreshold=4.25,
       lownoisethreshold=1.5, 
       minbeamfrac=0.3, 
       growiterations=75,
       negativethreshold=15.0,
       pbcor=True,
       restoringbeam='common',
       chanchunks=-1, # break up large cubes automatically so that you don't run out of memory.
       usepointing=False)


#13co
linevis = finalvis + '.contsub'
sourcename ='BHR71' # name of source
linename = '13co' # name of transition 
lineimagename = sourcename+'_'+linename # name of line image
spw = '1' # update to the spw you would like to image
restfreq='220.39868GHz'
start = '-8.6km/s'
width = '0.084km/s'
nchan = 100
outframe='lsrk' # velocity reference frame. See science goals.
veltype='radio' # velocity type.
field='4~17'
phasecenter=13
gridder='mosaic'
cell='0.20arcsec'
imsize = [450,450]
outframe='lsrk' # velocity reference frame. See science goals.
veltype='radio' # velocity type.
weighting = 'briggs'
robust=1
niter=10000
threshold = '0.0mJy'



#Cleaning 13co
tclean(vis=linevis,
       imagename=lineimagename, 
       field=field,
       spw=spw,
       phasecenter=phasecenter, # uncomment if mosaic or imaging an ephemeris object   
       mosweight = True, # uncomment if mosaic      
       specmode='cube', # comment this if observing an ephemeris source
       #specmode='cubesource', #uncomment this line if observing an ephemeris source
       perchanweightdensity=False, # uncomment if you are running in CASA >=5.5.0
       start=start,
       width=width,
       nchan=nchan, 
       outframe=outframe,
       veltype=veltype, 
       restfreq=restfreq, 
       niter=niter,  
       threshold=threshold, 
       interactive=True,
       cell=cell,
       imsize=imsize, 
       weighting=weighting,
       robust=robust,
       gridder=gridder,
       deconvolver='multiscale',
       scales=[0,5,10,15,20],#restart from beginning
       usemask='auto-multithresh',
       sidelobethreshold=2.0,
       noisethreshold=4.25,
       lownoisethreshold=1.5, 
       minbeamfrac=0.3, 
       growiterations=75,
       negativethreshold=15.0,
       pbcor=True,
       restoringbeam='common',
       chanchunks=-1, # break up large cubes automatically so that you don't run out of memory.
       usepointing=False)











#n2d+
linevis = finalvis + '.contsub'
sourcename ='BHR71' # name of source
linename = 'n2d+' # name of transition 
lineimagename = sourcename+'_'+linename # name of line image
spw = '3' # update to the spw you would like to image
restfreq='231.32183GHz'
start = '-8.6km/s'
width = '0.084km/s'
nchan = 100
outframe='lsrk' # velocity reference frame. See science goals.
veltype='radio' # velocity type.
field='4~17'
phasecenter=13
gridder='mosaic'
cell='0.20arcsec'
imsize = [450,450]
outframe='lsrk' # velocity reference frame. See science goals.
veltype='radio' # velocity type.
weighting = 'briggs'
robust=1
niter=10000
threshold = '0.0mJy'



#Cleaning n2d+
tclean(vis=linevis,
       imagename=lineimagename, 
       field=field,
       spw=spw,
       phasecenter=phasecenter, # uncomment if mosaic or imaging an ephemeris object   
       mosweight = True, # uncomment if mosaic      
       specmode='cube', # comment this if observing an ephemeris source
       #specmode='cubesource', #uncomment this line if observing an ephemeris source
       perchanweightdensity=False, # uncomment if you are running in CASA >=5.5.0
       start=start,
       width=width,
       nchan=nchan, 
       outframe=outframe,
       veltype=veltype, 
       restfreq=restfreq, 
       niter=niter,  
       threshold=threshold, 
       interactive=True,
       cell=cell,
       imsize=imsize, 
       weighting=weighting,
       robust=robust,
       gridder=gridder,
       deconvolver='multiscale',
       scales=[0,5,15,20,25],
       usemask='auto-multithresh',
       sidelobethreshold=2.0,
       noisethreshold=4.25,
       lownoisethreshold=1.5, 
       minbeamfrac=0.3, 
       growiterations=75,
       negativethreshold=15.0,
       pbcor=True,
       restoringbeam='common',
       chanchunks=-1, # break up large cubes automatically so that you don't run out of memory.
       usepointing=False)








#co
linevis = finalvis + '.contsub'
sourcename ='BHR71' # name of source
linename = 'co' # name of transition 
lineimagename = sourcename+'_'+linename # name of line image
spw = '2' # update to the spw you would like to image
restfreq='230.53800GHz'
start = '-29.6km/s'
width = '0.084km/s'
nchan = 600
outframe='lsrk' # velocity reference frame. See science goals.
veltype='radio' # velocity type.
field='4~17'
phasecenter=13
gridder='mosaic'
cell='0.20arcsec'
imsize = [450,450]
outframe='lsrk' # velocity reference frame. See science goals.
veltype='radio' # velocity type.
weighting = 'briggs'
robust=1
niter=100000
threshold = '0.0mJy'



#Cleaning co
tclean(vis=linevis,
       imagename=lineimagename, 
       field=field,
       spw=spw,
       phasecenter=phasecenter, # uncomment if mosaic or imaging an ephemeris object   
       mosweight = True, # uncomment if mosaic      
       specmode='cube', # comment this if observing an ephemeris source
       #specmode='cubesource', #uncomment this line if observing an ephemeris source
       perchanweightdensity=False, # uncomment if you are running in CASA >=5.5.0
       start=start,
       width=width,
       nchan=nchan, 
       outframe=outframe,
       veltype=veltype, 
       restfreq=restfreq, 
       niter=niter,  
       threshold=threshold, 
       interactive=True,
       cell=cell,
       imsize=imsize, 
       weighting=weighting,
       robust=robust,
       gridder=gridder,
       deconvolver='multiscale',
       scales=[0,5,15,20,25],
       usemask='auto-multithresh',
       sidelobethreshold=2.0,
       noisethreshold=4.25,
       lownoisethreshold=1.5, 
       minbeamfrac=0.3, 
       growiterations=75,
       negativethreshold=15.0,
       pbcor=True,
       restoringbeam='common',
       chanchunks=-1, # break up large cubes automatically so that you don't run out of memory.
       usepointing=False)



####################################################################
# Self Cal of Cont.


refant = 'DA49' # reference antenna. 
spwmap = [0,0] # mapping self-calibration solutions to individual spectral windows.



#Shallow Clean of Cont.
field='5~18'
phasecenter=10
gridder='mosaic'
cell='0.20arcsec'
imsize = [450,450]
outframe='lsrk' # velocity reference frame. See science goals.
veltype='radio' # velocity type.
weighting = 'briggs'
#robust=1
robust=0.5
niter=10000
#threshold = '0.0mJy'
threshold = '2mJy'


#Flagging before beginning clean
flagmanager(vis=contvis,mode='save',versionname='before_selfcal',merge='replace')



#Running tclean

contvis = 'calibrated_final_cont.ms'         
contimagename = 'BHR71_cont'

for ext in ['.image','.mask','.model','.image.pbcor','.psf','.residual','.pb','.sumwt','weight']:
    rmtables(contimagename + '_p0'+ ext)

tclean(vis=contvis,
       imagename=contimagename +'_p0',
       field=field,
       phasecenter=phasecenter, # uncomment if mosaic or imaging an ephemeris object
       mosweight=True, # uncomment if mosaic     
       specmode='mfs',
       #deconvolver='hogbom', 
       # Uncomment the below to image with nterms>1. Use if fractional bandwidth is >10%.
       #deconvolver='mtmfs',
       #nterms=2,
       imsize = imsize, 
       cell= cell, 
       weighting = weighting,
       robust = robust,
       niter = niter, #include multiscale cleaning
       threshold = threshold,
       interactive = True,
       deconvolver='multiscale',
       scales=[0,5,15,20,25],
       savemodel='modelcolumn', #need to add to all tclean for self-cal
       gridder = gridder,
       pbcor = True,
       usepointing=False)

#30 iterations
#Peak -> Max = 4.33e-01 J/beam, RMS = 2.13e-01
#Away from Peak -> Max = 6.67e-03, RMS = 2.52e-03
# SNR = Peak intensity/RMS_away -> 4.33e-01/2.52e-03 = 171.83





#Gaincal
rmtables('pcal1')
gaincal(vis=contvis,
        caltable='pcal1',
        field=field,
        gaintype='T',
        refant=refant,
        calmode='p',
        combine='spw',
        solint='inf',
        minsnr=3.0,
        minblperant=6)


#Plotting solutions (check for abnormalities)

plotcal(caltable='pcal1',
        xaxis='time',
        yaxis='phase',
        timerange='',
        iteration='antenna',
        subplot=421,
        figfile='pcal1Solution.png',
        plotrange=[0,0,-180,180])


#Apply solutions


applycal(vis=contvis,
     field=field,
     spwmap=spwmap,
     gaintable=['pcal1'],
     gainfield='nearest',
     calwt=False,
     flagbackup=False,
     interp='linearperobs')

#Flag 

flagmanager(vis=contvis,mode='save',versionname='after_pcal1')



# Deeper clean (do not clean to noise)



tclean(vis=contvis,
       imagename=contimagename + '_p1',
       field=field,
       phasecenter=phasecenter, # uncomment if mosaic or imaging an ephemeris object
       mosweight=True, # uncomment if mosaic     
       specmode='mfs',
       #deconvolver='hogbom', 
       # Uncomment the below to image with nterms>1. Use if fractional bandwidth is >10%.
       #deconvolver='mtmfs',
       #nterms=2,
       imsize = imsize, 
       cell= cell, 
       weighting = weighting,
       robust = robust,
       niter = niter, #include multiscale cleaning
       threshold = threshold,
       interactive = True,
       deconvolver='multiscale',
       scales=[0,5,15,20,25],
       gridder = gridder,
       pbcor = True,
       usepointing=False)

#150 iterations
#Peak -> Max = 1.53e-01 J/beam, RMS = 7.64e-02
#Away from Peak -> Max = 4.54e-03, RMS = 1.29e-03
# SNR = Peak intensity/RMS_away -> 1.53e-01/1.29e-03 = 118.60

















# To restart self-cal
# in CASA
# uncomment the following to revert to pre self-cal ms
# flagmanager(vis=contvis, mode='restore',versionname='before_selfcal')
# clearcal(contvis)
# delmod(contvis,field=field,otf=True)






