import numpy as np
from netCDF4 import Dataset
## functions originally written by Nick Szapiro,
## modified by Kelton Halbert.

def find_cells(file, lats_wrf, lons_wrf, degrees=False):
  '''
  Function to find the nearest MPAS cell to each gridpoint on a 
  WRF grid with lat/lon coordinates (in radians). 

  Parameters
  ----------
  file - the path to the file
  lats_wrf - the array of latitudes on the WRF grid
  lons_wrf - the array of longitudes on the WRF grid

  Returns
  -------
  cellIdx - an array containing the indices of the nearest MPAS
  cell to each WRF gridpoint.
  
  Original code by Nick Szapiro,
  modified by Kelton Halbert.
  '''
  ## if the lats/lons are passed through in degrees,
  ## convert them to radians
  if degrees:
    lats_wrf = np.radians(lats_wrf)
    lons_wrf = np.radians(lons_wrf)
  ## open the MPAS file and get the lon/lats of each cell
  data = Dataset(file, 'r')
  nEdgesOnCell = data.variables['nEdgesOnCell'][:];
  cellsOnCell = data.variables['cellsOnCell'][:]-1;
  latCell = data.variables['latCell'][:];
  lonCell = data.variables['lonCell'][:];
  data.close()
  
  #associate to nearest neighbor
  nPoints = len(lats_wrf)
  cellIdx = np.empty(nPoints, dtype=int); iCell=0
  pt_ll = np.empty(2,dtype=float)
  for iPt in xrange(nPoints):
    pt_ll[0] = lats_wrf[iPt]; pt_ll[1] = lons_wrf[iPt]
    ## find the index of the nearest cell to the gridpoint and return the index, then
    ## save it to the output array.
    iCell = findOwner_horizNbrs_latLon(pt_ll, iCell, latCell, lonCell, nEdgesOnCell, cellsOnCell)
    cellIdx[iPt] = iCell
  
  return cellIdx
  
def findOwner_horizNbrs_latLon(pt_ll, cellId, latCell, lonCell, nEdgesOnCell, cellsOnCell):
  '''
  Written by Nick Szapiro.
  '''
  dCell = calc_distSphere(1., pt_ll[0], pt_ll[1], latCell[cellId], lonCell[cellId]);

  flag = 1;
  while (flag==1):
    #keep going towards cell closer to point until no nbr is closer
    flag =0;
    nNbrs = nEdgesOnCell[cellId]
    nbrs = cellsOnCell[cellId,0:nNbrs]
    #nbrs = getNbrs_cell(cellId, nEdgesOnCell[cellId], cellsOnCell[cellId,:]);
    for i in range(nNbrs):
      nbrId = nbrs[i];
      dNbr = calc_distSphere(1., pt_ll[0], pt_ll[1], latCell[nbrId], lonCell[nbrId]);
      if (dNbr<dCell):
        dCell = dNbr;
        cellId = nbrId;
        flag=1;
      #running min
    #end of getting min of self and neighbors
  return(cellId);
  
def distSphere(radius, lat1, lon1, lat2, lon2):
  '''
  Calculates the distance between two points on a sphere, given
  its radius and the latitude/longitude (in radians)  of two points 
  on the sphere.

  Parameters
  ----------
  r - the radius of the sphere
  lat1 - the latitude of the first point
  lon1 - the longitude of the first point
  lat2 - the latitude of the second point
  lon2 - the longitude of the first point

  Returns
  -------
  dist - the distance between point 1 and point 2 (in meters)

  Original code by Nick Szapiro,
  modified by Kelton Halbert.
  '''
  
  dlat = lat2-lat1
  dlon = lon2-lon1
  latTerm = np.sin(.5*dlat); latTerm = latTerm*latTerm;
  lonTerm = np.sin(.5*dlon); lonTerm = lonTerm*lonTerm*np.cos(lat1)*np.cos(lat2);
  dAngle = np.sqrt(latTerm+lonTerm)
  dist = 2.*radius*np.arcsin(dAngle)
  
  return(dist)
  
