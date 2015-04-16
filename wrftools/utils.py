from wrftools.constants import *
from netCDF4 import Dataset
from wrftools import io
import numpy as np

__all__ = ["ncdump", "K2C", "C2K", "C2F", "F2C", "K2F", "F2K"]
__all__ = ['MS2KTS', 'KTS2MS', 'MS2MPH']
__all__ += ['MPH2MS', 'MPH2KTS', 'KTS2MPH', 'M2FT', 'FT2M']
__all__ += ['vec2comp', 'comp2vec', 'mag', 'QC']

def ncdump(filename):
    """
    Dump the contents of the netCDF file.
    """
    file = io.wrfopen(filename)
    print file
    for var in file.variables.keys():
        print file.variables[var]
    file.close()

def K2C(TMPK):
    """
    Take a scalar or an array of temperature values in degrees Kelvin
    and convert the scalar/array to degrees Celsius and return it.
    """
    return TMPK - ZEROCNK

def C2K(TMPC):
    """
    Take a scalar or an array of temperature values in degrees Celsius
    and convert the scalar/array to degrees Kelvin and return it
    """
    return TMPC + ZEROCNK

def C2F(TMPC):
    """
    Take a scalar or an array of temperature values in degrees Celsius
    and convert the scalar/array to degrees Fahrenheit and return it
    """
    return (1.8 * TMPC) + 32.

def F2C(TMPF):
    """
    Take a scalar or an array of temperature values in degrees Fahrenheit
    and convert the scalar/array to degrees Celsius and return it
    """
    return (TMPF - 32.) * (5. / 9.)

def K2F(TMPK):
    """
    Take a scalar or an array of temperature values in degrees Kelvin
    and convert the scalar/array to degrees Fahrenheit and return it
    """
    CT2F(KT2C(TMPK))

def F2K(TMPF):
    """
    Take a scalar or an array of temperature values in degrees Farhrenheit
    and conver the scalar/array to degrees Kelvin and return it
    """

def MS2KTS(val):
    """
    Take a scalar or an array of wind speeds in meters/second and convert
    them to knots and return it
    """
    return val * 1.94384449

def KTS2MS(val):
    """
    Take a scalar or an array of wind speeds in knots and convert them
    to meters/second and return it
    """
    return val * 0.514444

def MS2MPH(val):
    """
    Take a scalar or an array of wind speeds in meters/second and convert
    them to miles/hour and return it
    """
    return val * 2.23694

def MPH2MS(val):
    """
    Take a scalar or an array of wind speeds in miles/hour and convert
    them to meters/second and return it
    """
    return val * 0.44704

def MPH2KTS(val):
    """
    Take a scalar or an array of wind speeds in miles/hour and convert
    them to knots and return it
    """
    return val * 0.868976

def KTS2MPH(val):
    """
    Take a scalar or an array of wind speeds in knots and convert
    them to miles/hour and return it
    """
    return val * 1.15078

def M2FT(val):
    """
    Convert meters to feet
    """
    return val * 3.2808399

def FT2M(val):
    """
    Convert feet to meters
    """
    return val * 0.3048

