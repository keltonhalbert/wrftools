
def xy_to_gridpoint( x, y, gridx, gridy ):
    '''
    A function to find the nearest gridpoint to a given
    x/y coordinate (in meters).

    Parameters
    ----------
    lon - the x coordinate of a point
    lat - the y coordiante of a point
    gridx - the array of x values on the grid
    gridx - the array of y values on the grid
    
    Returns
    -------
    idx - the grid index of the nearest point
    '''
    distance = ( gridx - x )**2 + ( gridy - y )**2  
    idx = np.where( distance == distance.min() )[0]
    return idx
