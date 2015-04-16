import wrftools.utils as utils
import wrftools.io as io
import numpy

__all__ = ["wspd", "wspdkts", "wspdmph"]

def wspd(wrf_file):
    """
    Calculate the wind speed in m/s from
    the WRF output file.
    """
    wrf_nc_file = io.wrfopen(wrf_file)
    U = wrf_nc_file.variables["U"][:]
    V = wrf_nc_file.variables["V"][:]
    wrf_nc_file.close()
    return numpy.sqrt(numpy.power(U, 2) + numpy.power(V, 2))

def wspdkts(wrf_file):
    """
    Calculate the wind speed in knots
    from the WRF output file.
    """
    return utils.MS2KTS(wspd(wrf_file))

def wspdmph(wrf_file):
    """
    Calculate the wind speed in miles/hour
    from the WRF output file.
    """
    return utils.MS2MPH(wspd(wrf_file))


