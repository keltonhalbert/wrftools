## Written by Kelton Halbert // January 2014
## keltonhalbert@ou.edu
## http://tempestchasing.com
## Protected under the GPL V2 License

from netCDF4 import Dataset
import numpy

__all__ = ['wrf_theta', 'wrf_temp', 'wrf_rh', 'wrf_dewp']

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
