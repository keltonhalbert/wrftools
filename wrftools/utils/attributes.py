## Written by Kelton Halbert // January 2014
## keltonhalbert@ou.edu
## http://tempestchasing.com
## Protected under the GPL V2 License

from wrftools.variables import *
from wrftools.utils import *
from wrftools.interp import *
from netCDF4 import Dataset
import numpy

def wrf_copy_attributes( infilename, outfilename ):
    ## open the files
    infile = Dataset( infilename )
    outfile = Dataset( outfilename, 'w', format='NETCDF4' )
    
    ## create dimensions
    level = outfile.createDimension( 'bottom_top', None )
    time = outfile.createDimension( 'time', None )
    lon = outfile.createDimension( 'south_north', infile.getncattr('SOUTH-NORTH_PATCH_END_UNSTAG') )
    lat = outfile.createDimension( 'west_east', infile.getncattr('WEST-EAST_PATCH_END_UNSTAG') )
    
    ## copy the global attributes to the new file
    inattrs = infile.ncattrs()
    for attr in inattrs:
        outfile.setncattr( attr, infile.getncattr( attr ) )
    infile.close()
    outfile.close()
    
def wrf_copy_sfc_fields( infilename, outfilename ):
    
    infile = Dataset( infilename )
    outfile = Dataset( outfilename, 'a' )
    
    T2 = outfile.createVariable( 'T2', 'f4', ('time', 'south_north', 'west_east') )
    TH2 = outfile.createVariable( 'TH2', 'f4', ('time', 'south_north', 'west_east') )
    Q2 = outfile.createVariable( 'Q2', 'f4', ('time', 'south_north', 'west_east') )
    PSFC = outfile.createVariable( 'PSFC', 'f4', ('time', 'south_north', 'west_east') )
    U10 = outfile.createVariable( 'U10', 'f4', ('time', 'south_north', 'west_east') )
    V10 = outfile.createVariable( 'V10', 'f4', ('time', 'south_north', 'west_east') )
    SNOWH = outfile.createVariable( 'SNOWH', 'f4', ('time', 'south_north', 'west_east') )
    SEAICE = outfile.createVariable( 'SEAICE', 'f4', ('time', 'south_north', 'west_east') )
    RAINNC = outfile.createVariable( 'RAINNC', 'f4', ('time', 'south_north', 'west_east') )
    SNOWNC = outfile.createVariable( 'SNOWNC', 'f4', ('time', 'south_north', 'west_east') )
    REFL_10CM = outfile.createVariable( 'REFL_10CM', 'f4', ('time', 'south_north', 'west_east') )
    DEW2 = outfile.createVariable( 'DEWP', 'f4', ('time', 'south_north', 'west_east') )
    RH2 = outfile.createVariable( 'RH2', 'f4', ('time', 'south_north', 'west_east') )
    OLR = outfile.createVariable( 'OLR', 'f4', ('time', 'south_north', 'west_east') )
    
    OLR[:] = infile.variables['OLR'][:]
    T2[:] = infile.variables['T2'][:]
    TH2[:] = infile.variables['TH2'][:]
    Q2[:] = infile.variables['Q2'][:]
    RH2[:] = wrf_rh( infile.variables['T2'][:], infile.variables['PSFC'][:]*.01, infile.variables['Q2'][:] )
    PSFC[:] = infile.variables['PSFC'][:] * .01
    U10[:] = infile.variables['U10'][:]
    V10[:] = infile.variables['V10'][:]
    SNOWH[:] = infile.variables['SNOWH'][:]
    SEAICE[:] = infile.variables['SEAICE'][:]
    RAINNC[:] = infile.variables['RAINNC'][:]
    SNOWNC[:] = infile.variables['SNOWNC'][:]
    REFL_10CM[:] = infile.variables['REFL_10CM'][ :, 0, :, : ]
    DEW2[:] = wrf_dewp( infile.variables['T2'][:], infile.variables['PSFC'][:]*.01, infile.variables['Q2'][:] )[:]
    
    infile.close()
    outfile.close()

def wrf_copy_static_fields( infilename, outfilename ):
    
    infile = Dataset( infilename )
    outfile = Dataset( outfilename, 'a' )
    
    XLONG = outfile.createVariable( 'XLONG', 'f4', ('south_north', 'west_east') )
    XLAT = outfile.createVariable( 'XLAT', 'f4', ('south_north', 'west_east') )


    SINALPHA = outfile.createVariable( 'SINALPHA', 'f4', ('south_north', 'west_east') )
    COSALPHA = outfile.createVariable( 'COSALPHA', 'f4', ('south_north', 'west_east') )
    MAPFAC_M = outfile.createVariable( 'MAPFAC_M', 'f4', ('south_north', 'west_east') )
    F = outfile.createVariable( 'F', 'f4', ('south_north', 'west_east') )
    MU = outfile.createVariable( 'MU', 'f4', ('south_north', 'west_east') )
    MUB = outfile.createVariable( 'MUB', 'f4', ('south_north', 'west_east') )
    XTIME = outfile.createVariable( 'XTIME', 'f4', ('time') )
    try:
        XLONG[:] = infile.variables['XLONG'][0][:]
        XLAT[:] = infile.variables['XLAT'][0][:]
        F[:] = infile.variables['F'][0][:]
        MU[:] = infile.variables['MU'][0][:]
        MUB[:] = infile.variables['MUB'][0][:]

        MAPFAC_M[:] = infile.variables['MAPFAC_M'][0][:]
        SINALPHA[:] = infile.variables['SINALPHA'][0][:]
        COSALPHA[:] = infile.variables['COSALPHA'][0][:]
        XTIME[:] = infile.variables['XTIME'][:]

    except:
        XLONG[:] = infile.variables['XLONG'][:]
        XLAT[:] = infile.variables['XLAT'][:]
        F[:] = infile.variables['F'][:]
        MU[:] = infile.variables['MU'][:]
        MUB[:] = infile.variables['MUB'][:]

        MAPFAC_M[:] = infile.variables['MAPFAC_M'][:]
        SINALPHA[:] = infile.variables['SINALPHA'][:]
        COSALPHA[:] = infile.variables['COSALPHA'][:]
        XTIME[:] = infile.variables['XTIME'][:]
    infile.close()
    outfile.close()

def wrf_unstagger( grid, dim ):
    """ Unstagger a staggered WRF grid in the X, Y, or Z (U, V, or W) direction.
        ---------------------
        grid (numpy.ndarray): The 2D, 3D, 4D, or 5D array to be unstaggered.
        dim (str): A string specifying what dimension to unstagger. Must be
        X, Y, Z, U, V or W.
        ---------------------
        returns:
        numpy.ndarray unstaggered grid (dim-1)
        ---------------------
        EXAMPLE:
        import numpy as np
        
        arr = np.random.randint( low=1, high=10, size=( 9,10,9 ) ) ## create a random array staggered in the Y direction
        arr_unstaggered = wrf_unstagger( arr, 'Y' )
        """
    nd = len( grid.shape )
    if dim == 'X' or dim == 'U':
        if nd == 5:
            gridout = ( grid[ :, :, :, :, :-1 ] + grid[ :, :, :, :, 1: ] ) / 2
        elif nd == 4:
            gridout = ( grid[ :, :, :, :-1 ] + grid[ :, :, :, 1: ] ) / 2
        elif nd == 3:
            gridout = ( grid[ :, :, :-1 ] + grid[ :, :, 1: ] ) / 2
        elif nd == 2:
            gridout = ( grid[ :, :-1 ] + grid[ :, 1: ] ) / 2
        else: pass
    if dim == 'Y' or dim == 'V':
        if nd == 5:
            gridout = ( grid[ :, :, :, :-1, : ] + grid[ :, :, :, 1:, : ] ) / 2
        elif nd == 4:
            gridout = ( grid[ :, :, :-1, : ] + grid[ :, :, 1:, : ] ) / 2
        elif nd == 3:
            gridout = ( grid[ :, :-1, : ] + grid[ :, 1:, : ] ) / 2
        elif nd == 2:
            gridout = ( grid[ :-1, : ] + grid[ 1:, : ] ) / 2
        else: pass
    if dim == 'Z' or dim == 'W':
        if nd == 5:
            gridout = ( grid[ :, :, :-1, :, : ] + grid[ :, :, 1:, :, : ] ) / 2
        elif nd == 4:
            gridout = ( grid[ :, :-1, :, : ] + grid[ :, 1:, :, : ] ) / 2
        elif nd == 3:
            gridout = ( grid[ :-1, :, : ] + grid[ 1:, :, : ] ) / 2
        else: pass
    return gridout
