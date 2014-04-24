## Written by Kelton Halbert // January 2014
## keltonhalbert@ou.edu
## http://tempestchasing.com
## Protected under the GPL V2 License

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
#    except: pass
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

def wrf_pressure( P, PB ):
    """ Calculate the pressure in hPa given Perturbation Pressure (P) and Base State Pressure (PB) in Pa.
    ---------------------
    P (numpy.ndarray): ndarray of Perturbation Pressure from WRF 
    PB (numpy.ndarray): ndarray of Base State Pressure from WRF
    ---------------------
    returns:
        numpy.ndarray of pressure in hPa the same shape as P and PB 
        """
    assert P.shape == PB.shape, 'Arrays are different shapes. They must be the same shape.'
    return ( P + PB ) * .01

def wrf_height( PH, PHB ):
    """ Calculate the geopotential height given the Perturbation Geopotential (PH) and the Base State
        Geopotential (PHB). PH and PHB must be the same shape. 
    ---------------------
    PH (numpy.ndarray): ndarray of Perturbation Geopotential from WRF
    PHB (numpy.ndarray): ndarray of Base State Geopotential from WRF
    ---------------------
    returns:
        numpy.ndarray of geopotential height in meters in sane shape as PH and PHB
        """
    assert PH.shape == PHB.shape, 'Arrays are different shapes. They must be the same shape.'
    return ( PH + PHB ) / 9.81

def wrf_theta( T ):
    """ Calculate the potential temperature given the Perturbation Potential Temperature (T) in degrees Kelvin.
    ---------------------
    T (numpy.ndarray): ndarray of Perturbation Potential Temperature from WRF
    ---------------------
    returns:
        numpy.ndarray of potential temperature in degrees Kelvin, same shape as T
        """
    return T + 300

def wrf_temp( THETA, PRES ):
    """ Calculate the 'normal' temperature in degrees Kelvin given the 
    Potential Temperature (THETA in Kelvin) and Pressure (PRES in hPa or mb).
    PRES and THETA must be the same shape.
    ---------------------
    THETA (numpy.ndarray): ndarray of potential temperature in degrees Kelvin
    PRES (numpy.ndarray): ndarray of pressure in hPa or mb same shape as THETA
    ---------------------
    returns:
        numpy.ndarray of 'normal' temperature in degrees Kelvin same shape as THETA and PRES
        """
    assert THETA.shape == PRES.shape, 'Arrays are different shapes. They must be the same shape.'
    K = 0.2854
    return THETA * ( PRES / 1000 )**K

def wrf_rh( TEMP, PRES, QVAPOR ):
    """ Calculate relative humidity given the Temperature in Kelvin (TEMP), 
    Pressure in hPa or mb (PRES), and Water Vapor Mixing Ratio (QVAPOR).
    TEMP, PRES, and QVAPOR must be the same shape.
    ---------------------
    TEMP (numpy.ndarray): ndarray of 'normal' temperature in degrees Kelvin
    PRES (numpy.ndarray): ndarray of pressure in hPa or mb same shape as TEMP
    QVAPOR (numpy.ndarray): ndarray of Water Vapor Mixing Ratio from WRF, same shape as PRES and TEMP
    ---------------------
    returns:
        numpy.ndarray of relative humidity values (%) same shape as TEMP, PRES, and QVAPOR
        """
    assert TEMP.shape == PRES.shape == QVAPOR.shape, 'Arrays are different shapes. They must be the same shape.'
    e_0 = 6.1173 ## mb
    t_0 = 273.16 ## K
    Rv = 461.50 ## J K-1 Kg-1
    Lv_0 = 2.501 * 10**6 ## J Kg-1
    K1 = Lv_0 / Rv ## K 
    K2 = 1 / t_0 ## K-1
    K3 = 1 / TEMP ## K-1
    ## Clausius Clapeyron Equation
    e_s = e_0 * numpy.exp( K1 * ( K2 - K3 ) )
    w_s = ( 0.622 * e_s ) / ( PRES - e_s )
    return ( QVAPOR / w_s ) * 100

def wrf_dewp( TEMP, PRES, QVAPOR ):
    """ Calculate the dewpoint temperature in Celsius given the
	Temperature (TEMP), Pressure (PRES), and Mixing Ratio
	(QVAPOR). Arrays must be the same shape.

    ---------------------
    TEMP (numpy.ndarray): ndarray of 'normal' temperature in degrees Kelvin
    ---------------------
    returns:
        numpy.ndarray of dewpoint values (c) same shape as TEMP, PRES, and QVAPOR
	"""
    ## constants for the Clausius Clapeyron Equation
    e_0 = 6.1173 ## mb
    t_0 = 273.16 ## K
    Rv = 461.50 ## J K-1 Kg-1
    Lv_0 = 2.501 * 10**6 ## J Kg-1
    ## Compute portions of the equation
    K1 = Lv_0 / Rv ## K 
    K2 = 1 / t_0 ## K-1
    K3 = 1 / TEMP ## K-1
    ## Clausius Clapeyron Equation
    e_s = e_0 * numpy.exp( K1 * ( K2 - K3 ) ) ## mb
    ## get saturation mixing ratio for RH
    w_s = ( 0.622 * e_s ) / ( PRES - e_s )
    rh = ( QVAPOR / w_s ) * 100
    ## back out the vapor pressure
    e = ( rh / 100 ) * e_s ## mb
    ## compute individual terms when solving the equation for Td
    K1_inv = Rv / Lv_0
    K4 = numpy.log( e / e_0 )
    term1 = K2 - (K1_inv * K4)
    return 1 / term1





def wrf_vort( U, V, dx ):
    """Calculate the relative vorticity given the U and V vector components in m/s
    and the grid spacing dx in meters.
    U and V must be the same shape.
    ---------------------
    U (numpy.ndarray): ndarray of U vector values in m/s
    V (numpy.ndarray): ndarray of V vector values in m/s
    dx (float or int): float or integer of U and V grispacing in meters
    ---------------------
    returns:
        numpy.ndarray of vorticity values s^-1 same shape as U and V
    """
    assert U.shape == V.shape, 'Arrays are different shapes. They must be the same shape.'
    dy = dx
    du = numpy.gradient( U )
    dv = numpy.gradient( V )
    return ( dv[-1]/dx - du[-2]/dy )

def wrf_absvort( U, V, F, dx ):
    """Calculate the absolute vorticity given the U and V vector components in m/s,
    the Coriolis sine latitude term (F) in s^-1, and gridspacing dx in meters. U, V, and F
    must be the same shape.
    ---------------------
    U (numpy.ndarray): ndarray of U vector values in m/s
    V (numpy.ndarray): ndarray of V vector values in m/s
    F (numpy.ndarray): ndarray of Coriolis sine latitude values in s^-1
    dx (float or int): float or integer of U and V grispacing in meters
    ---------------------
    returns:
        numpy.ndarray of absolute vorticity values s^-1 same shape as U and V
    
    """
    assert U.shape == V.shape, 'Arrays are different shapes. They must be the same shape.'
    return wrf_vort( U, V, dx ) + F

def wrf_pv( U, V, F, THETA, PRES, MAPFAC_M, dx ):
    """Calculate the potential vorticity given the U and V vector components in m/s,
    the Coriolis sine latitude term (F) in s^-1, THETA potential temperature in degrees
    Kelvin, PRES pressure in hPa or mb, the map scale factor on mass grid and the gridspacing 
    dx in meters. U, V, F, THETA, and PRES must be 4D arrays.
    ---------------------
    U (numpy.ndarray): ndarray of U vector values in m/s
    V (numpy.ndarray): ndarray of V vector values in m/s
    F (numpy.ndarray): ndarray of Coriolis sine latitude values in s^-1
    THETA (numpy.ndarray): ndarray of potential temperature in degrees Kelvin
    PRES (numpy.ndarray): ndarray of pressure in hPa or mb same shape as THETA
    MAPFAC_M (numpy.ndarray): 2D of map scale factor on mass grid. 
    dx (float or int): float or integer of U and V grispacing in meters
    ---------------------
    returns:
        numpy.ndarray of potential vorticity values in ( K * m^2 * kg^-1 * s^-1 ) * 10^6 
        ( or 1 PVU * 10^6).
    """
    assert U.shape == V.shape == THETA.shape == PRES.shape, 'Arrays are different shapes. They must be the same shape.'
    ## pres in hPa needs to convert to Pa
    PRES = PRES * 100
    dx = dx * MAPFAC_M
    dy = dx
    grav = 9.8

    dVt,dVp,dVy,dVx = numpy.gradient( V )
    dUt,dUp,dUy,dUx = numpy.gradient( U )
    dTt,dTp,dTy,dTx = numpy.gradient( THETA )
    dPt,dp,dPy,dPx = numpy.gradient( PRES )
    return ( -grav * ( -dVp/dp * dTx/dx + dUp/dp * dTy/dy + ( dVx/dx - dUy/dy + F ) * dTp/dp ) ) * pow(10, 6)
