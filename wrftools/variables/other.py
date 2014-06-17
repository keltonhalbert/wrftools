import numpy
from netCDF4 import Dataset
def wrf_slp( infilename, outfilename ):
    infile = Dataset( infilename )
    outfile = Dataset( outfilename, 'a' )            
    stemps = infile.variables['T2'][:]+6.5*infile.variables['HGT'][:]/1000.
    SLP_in = infile.variables['PSFC'][:]*numpy.exp(9.81/(287.0*stemps)*infile.variables['HGT'][:])*0.01 + (6.7 * infile.variables['HGT'][:] / 1000)
    SLP = outfile.createVariable( 'SLP', 'f4', ('time', 'south_north', 'west_east') )
    SLP[:] = SLP_in    
    infile.close()
    outfile.close() 
