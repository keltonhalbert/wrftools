from wrftools.variables import * 
from wrftools.utils import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from interp_pv import *
import numpy as np
from mpl_toolkits.basemap import Basemap
infile = Dataset('/raid2/kelton/arcticwrf/wrfout/raw/wrfout_d01_2015-02-12_00:00:00')

print 'I am now moving on to metr fields'
PRES_in = wrf_pressure( infile.variables['P'][:], infile.variables['PB'][:] )
print 'One'
HGHT_in = wrf_unstagger( wrf_height( infile.variables['PH'][:], infile.variables['PHB'][:] ), 'Z' )
print 'Two'
THETA_in = wrf_theta( infile.variables['T'][:] )

print 'Three'
U_in = wrf_unstagger( infile.variables['U'][:], 'U' )
V_in = wrf_unstagger( infile.variables['V'][:], 'V' )

print "PV time"
PV_in = wrf_pv( U_in, V_in, infile.variables['F'][0][:], THETA_in, PRES_in, infile.variables['MAPFAC_M'][0][:], infile.DX )

interplevels = np.array([0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0])
#interplevels = np.array([1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0])
print len(interplevels)

print PV_in.shape
#out = np.ones((PV_in.shape[0], interplevels.shape[0], PV_in.shape[2], PV_in.shape[3]), dtype=np.float64)
out = interp_pv(PV_in, THETA_in, interplevels)

m = Basemap( projection='npstere', boundinglat=25, lon_0=-100, resolution='l' )
for i in xrange(0,21,1):
	print out[i, 3, :, :].shape, out[i, 3, :, :].max(), out[i, 3, :, :].min()
	plt.figure(figsize=(10,10), dpi=200)
	m.drawcoastlines()
	m.drawcountries()
	m.drawstates()
	cm = m.imshow(out[i, 3, :, :], vmin=275, vmax=390, cmap=plt.get_cmap('RdYlBu_r'))
	plt.colorbar(cm)
	plt.savefig("MyFirstFortranWrappedProgramInPython" + str(i) + ".png")
	plt.close()	
	
	
	
	
	
	
	
