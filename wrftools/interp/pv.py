## Written by Kelton Halbert // January 2014
## keltonhalbert@ou.edu
## http://tempestchasing.com
## Protected under the GPL V2 License

import numpy

def wrf_to_pv( grid, surface, interplevels ):
    """Linearly interpolates a grid to potential voericity levels defined by 
        interplevels. This uses the numpy.interp function that requires
        the function coordinate values to be monotonically increasing,
        and this function does not check for this. See numpy.interp docs
        for more information. Grid and surface must be the same shape.
    -----------------------
    grid (numpy.ndarray): 4D array of values to be interpolated onto a vertical surface.  Must be monotonically increasing.
    surface (numpy.ndarray): 4D array of the verical coordinate values of the surface to be interpolated to. Must be monotonically increasing.
    interplevels (numpy.ndarray): 1D array of vertical coordinate values that are desired to be interpolated to.
    -----------------------
    returns:
        numpy.ndarray of values of shape (grid.shape[0], len( interplevels ), grid.shape[2], grid.shape[3] )
    """
    shape = ( grid.shape[0], interplevels.shape[0], grid.shape[2], grid.shape[3] )
    outgrid = numpy.ones( shape )
    for time in numpy.arange( grid.shape[0] ):
        for idx, val in numpy.ndenumerate( grid[0][0] ):
            column = surface[ time, :, idx[0], idx[1] ]
            column_GRID = grid[ time, :, idx[0], idx[1] ]
            pvidx = numpy.where( column < interplevels[0] )[0]
            if len( pvidx ) == 0:
                pvidx = numpy.where( column < interplevels[1] ) [0]
            else:
                pvidx = pvidx
            try:
                value = numpy.interp( interplevels, column[ pvidx[-1] : ], column_GRID[ pvidx[-1] : ], left=numpy.nan, right=numpy.nan )
                outgrid[ time, :, idx[0], idx[1] ] = value[:]
            except:
                value = numpy.interp( interplevels, column, column_GRID, left=numpy.nan, right=numpy.nan )
                outgrid[ time, :, idx[0], idx[1] ] = value[:]
    return outgrid
