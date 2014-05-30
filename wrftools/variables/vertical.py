## Written by Kelton Halbert // January 2014
## keltonhalbert@ou.edu
## http://tempestchasing.com
## Protected under the GPL V2 License

from netCDF4 import Dataset
import numpy

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