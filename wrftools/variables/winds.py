## Written by Kelton Halbert // January 2014
## keltonhalbert@ou.edu
## http://tempestchasing.com
## Protected under the GPL V2 License

from netCDF4 import Dataset
import numpy

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
