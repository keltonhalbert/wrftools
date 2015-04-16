from wrftools.variables.standard import *
import wrftools.utils as utils
import wrftools.io as io
import numpy as np

__all__ = ["theta", "tmpc", "tmpf", "tmpk", "dwpk", "dwpf", "dwpc", "satvap", "relh"]

def theta(wrf_file):
    """
    Calculate potential temperature from the 
    WRF model output.
    """
    wrf_nc_file = io.wrfopen(wrf_file)
    theta = wrf_nc_file.variables["T"][:] + 300.
    wrf_nc_file.close()
    return theta

def tmpk(wrf_file):
    """
    Calculate the tempreature in degrees Kelvin
    from the WRF model output.
    """
    return theta(wrf_file) * ( pres(wrf_file) / 1000. )**ROCP

def tmpc(wrf_file):
    """
    Calculate the temperature in degrees Celsius
    from the WRF model output.
    """
    utils.K2C(tmpk(wrf_file))

def tmpf(wrf_file):
    """
    Calculate the temperautre in degrees Fahrenheit
    from the WRF model output.
    """
    utils.K2F(tmpk(wrf_file))

def satvap(wrf_file):
    """
    Calculate the saturation vapor pressure
    from the WRF output
    """
    e_0 = 6.1173 ## mb
    Rv = 461.50 ## J K-1 Kg-1
    Lv_0 = 2.501 * 10**6 ## J Kg-1

    K1 = Lv_0 / Rv ## K
    K2 = 1 / ZEROCNK ## K-1
    K3 = 1 / tmpk(wrf_file) ## K-1

    ## Clausius Clapeyron Equation
    e_s = e_0 * numpy.exp( K1 * ( K2 - K3 ) )
    return e_s

def relh(wrf_file):
    """
    Calculate the relative humidity from the WRF
    model output.
    """
    wrf_nc_file = io.wrfopen(wrf_file)

    e_s = satvap(wrf_file)
    w_s = ( 0.622 * e_s ) / ( pres(wrf_file) - e_s )
    qvapor = wrf_nc_file.variables["QVAPOR"][:]
    wrf_nc_file.close()

    return ( qvapor / w_s ) * 100

def dwpk(wrf_file):
    """
    Calculate the dewpoint temperature from the WRF
    model output.
    """
     ## constants for the Clausius Clapeyron Equation
    e_0 = 6.1173 ## mb
    Rv = 461.50 ## J K-1 Kg-1
    Lv_0 = 2.501 * 10**6 ## J Kg-1
    ## Compute portions of the equation
    K2 = 1 / ZEROCNK ## K-1

    e_s = satvap(wrf_file) 
    rh = relh(wrf_infile)
    ## back out the vapor pressure
    e = ( rh / 100 ) * e_s ## mb
    ## compute individual terms when solving the equation for Td
    K1_inv = Rv / Lv_0
    K4 = numpy.log( e / e_0 )
    term1 = K2 - (K1_inv * K4)
    return 1 / term1

def dwpc(wrf_file):
    """
    Calculate the dowpoint temperature in degrees
    Celsius from the WRF output.
    """
    return utils.K2C(dwpk(wrf_file))

def dwpf(wrf_file):
    """
    Calculate the dewpoint temperature in degrees
    Fahrenheit from the WRF output.
    """
    return utils.K2F(dwpk(wrf_file))

