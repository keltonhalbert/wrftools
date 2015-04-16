from wrftools.constants import *
import wrftools.io as io
import numpy as np

__all__ = ["hght", "pres"]

def hght(wrf_file):
    """
    Compute the Geopotential Height (m)
    from the WRF dataset.
    """
    wrf_nc_file = io.wrfopen(wrf_file)
    hght = (wrf_nc_file.variables['PH'][:] + wrf_nc_file.variables['PHB'][:]) / G
    wrf_nc_file.close()
    return hght

def pres(wrf_file):
    """
    Compute the Pressure (hPa) from 
    the WRF dataset
    """
    wrf_nc_file = io.wrfopen(wrf_file)
    pres = (wrf_nc_file.variables["P"][:] + wrf_nc_file.variables["PB"][:]) * .01
    wrf_nc_file.close()
    return pres

