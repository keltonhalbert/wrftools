## Written by Kelton Halbert // January 2014
## keltonhalbert@ou.edu
## http://tempestchasing.com
## Protected under the GPL V2 License

import numpy

def wrf_to_pres( grid, surface, interplevels ):
    '''
    Linearly interpolates a grid to interplevels. This uses the 
    numpy.interp function that requires the function coordinate 
    values to be monotonically increasing, and this function does 
    not check for this. See numpy.interp docs for more information. 
    Grid and surface must be the same shape.

    Parameters
    ----------
    grid - 4D array of values to be interpolated onto a vertical surface.  
        Must be monotonically increasing.
    surface - 4D array of the verical coordinate values of the surface to be 
        interpolated to. Must be monotonically increasing.
    interplevels - 1D array of vertical coordinate values that are desired 
        to be interpolated to.

    Returns
    -------
    outgrid - numpy.ndarray of values of shape 
        (grid.shape[0], len( interplevels ), grid.shape[2], grid.shape[3] )
    '''
    ## get the shape of the original grid but with the vertical dimension of
    ## interplevels, and then allocate an empty array based on that shape.
    shape = ( grid.shape[0], interplevels.shape[0], grid.shape[2], grid.shape[3] )
    outgrid = numpy.empty( shape )
    ## loop through the time dimemsion of the array
    for time in numpy.arange( grid.shape[0] ):
        ## loop over each gridpoint and get the vertical column
        for idx, val in numpy.ndenumerate( grid[0][0] ):
            ## get the column slice of pressure
            column = surface[ time, :, idx[0], idx[1] ]
            ## get the column slice of the value to interpolate
            column_GRID = grid[ time, :, idx[0], idx[1] ]
            ## interpolate a whole column of valyes and add it to the new array
            value = numpy.interp( interplevels, column, column_GRID, left=numpy.nan, right=numpy.nan )
            outgrid[ time, :, idx[0], idx[1] ] = value[:]
    return outgrid

