## Written by Kelton Halbert // May 2014
## keltonhalbert@ou.edu
## http://tempestchasing.com
## Protected under the GPL V2 License

import numpy

def ft_to_m( dist ):
    '''
    Converts feet to meters. 
    
    Parameters
    ----------
    dist: an int, float, or array of int/float whose units
    are in feet.
    
    Returns
    -------
    dist converted to meters.
    '''
    return dist / 3.2808

def m_to_ft( dist ):
    '''
    Converts meters to feet.
    
    Parameters
    ----------
    dist: an int, float, or array of int/float whose units
    are in meters.
    
    Returns
    -------
    dist converted to feet.
    '''

    return dist * 3.2808

def k_to_c( tmp ):
    '''
    Converts Kelvin to Celsius.
    
    Parameters
    ----------
    tmp: an int, float, or array of int/float whose units
    are in degrees Kelvin.
    
    Returns
    -------
    tmp converted to degrees Celsius.
    '''
    return tmp - 273.15

def c_to_k( tmp ):
    '''
    Converts Celsius to Kelvin.
    
    Parameters
    ----------
    tmp: an int, float, or array of int/float whose units
    are in degrees Celsius.
    
    Returns
    -------
    tmp converted to degrees Kelvin
    '''
    return val + 273.15

def c_to_f( tmp ):
    '''
    Converts Celsius to Fahrenheit.
    
    Parameters
    ----------
    tmp: an int, float, or array of int/float whose units
    are in degrees Celsius.
    
    Returns
    -------
    tmp converted to degrees Fahrenheit.
    '''
    return tmp * (9./5.) + 32.

def f_to_c( tmp ):
    '''
    Converts Fahrenheit to Celsius.
    
    Parameters
    ----------
    tmp: an int, float, or array of int/float whose units
    are in degrees Fahrenheit.
    
    Returns
    -------
    tmp converted to degrees Celsius.
    '''
    return (tmp - 32.) * (5./9.)

def k_to_f( tmp ):
    '''
    Converts Kelvin to Fahrenheit.
    
    Parameters
    ----------
    tmp: an int, float, or array of int/float whose units
    are in degrees Kelvin.
    
    Returns
    -------
    tmp converted to degrees Fahrenheit.
    '''
    tmp = k_to_c( tmp )
    return c_to_f( tmp )

def f_to_k( tmp ):
    '''
    Converts Fahrenheit to Kelvin.
    
    Parameters
    ----------
    tmp: an int, float, or array of int/float whose units
    are in degrees Fahrenheit.
    
    Returns
    -------
    tmp converted to degrees Kelvin
    '''
    tmp = f_to_c( tmp )
    return c_to_k( tmp )

def ms_to_mh( spd ):
    '''
    Converts meters/second to miles/hour.
    
    Parameters
    ----------
    spd: an int, float, or array of int/float whose units
    are in meters/second.
    
    Returns
    -------
    spd converted to miles/hour.
    '''
    return spd * 0.00062137 * 3600.

def mh_to_ms( spd ):
    '''
    Converts miles/hour to meters/second.
    
    Parameters
    ----------
    spd: an int, float, or array of int/float whose units
    are in miles/hour.
    
    Returns
    -------
    spd converted to meters/second
    '''
    return spd / * 0.00062137 / 3600.

def mh_to_kts( spd ):
    '''
    Converts miles/hour to knots.
    
    Parameters
    ----------
    spd: an int, float, or array of int/float whose units
    are in mile/hour
    
    Returns
    -------
    spd converted to knots.
    '''
    return spd * (5280./6076.)

def kts_to_mh( spd ):
    '''
    Converts knots to miles/hour.
    
    Parameters
    ----------
    spd: an int, float, or array of int/float whose units
    are in knots.
    
    Returns
    -------
    spd converted to miles/hour
    '''
    return spd * (6076./5280.)

def ms_to_kts( spd ):
    '''
    Converts meters/second to knots.
    
    Parameters
    ----------
    spd: an int, float, or array of int/float whose units
    are in meters/second.
    
    Returns
    -------
    spd converted to knots.
    '''
    spd = ms_to_mh( spd )
    return mh_to_kts( spd )

def kts_to_ms( spd ):
    '''
    Converts knots to meters/second.
    
    Parameters
    ----------
    spd: an int, float, or array of int/float whose units
    are in knots.
    
    Returns
    -------
    spd converted to meters/second
    '''
    spd = kts_to_mh( spd )
    return mh_to_ms( spd )



