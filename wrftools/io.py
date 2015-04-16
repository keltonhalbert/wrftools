from netCDF4 import Dataset, MFDataset
import numpy as np
import gc

def wrfopen(file, mode="r", ncformat=None):
    """
    Open a new WRF file or list of files for 
    processing. File(s) are assumed to be an 
    output file from a successful model run.
    """
    if ncformat == None: ncformat = "NETCDF3_CLASSIC"
    if type(file) == list:
        wrf_ncfile = MFDataset(file, mode, format=ncformat)
    else:
        wrf_ncfile = Dataset(file, mode, format=ncformat)
    return wrf_ncfile

def copy_all_dimensions(wrf_infile, wrf_outfile):
    """
    Copy the dimensions from an input wrf file to 
    an output wrf file. wrf_infile and wrf_outfile
    are assumed to be strings containing the paths
    to existing input and output files.
    """
    ## open the files
    wrf_nc_infile = wrfopen(wrf_infile)
    wrf_nc_outfile = wrfopen(wrf_outfile, mode="a", ncformat=wrf_nc_infile.data_model)
    ## get the list of dimensions in the  input file,
    ## then loop over them and create a corresponding
    ## dimension in the output file using the function
    ## included in this package
    dimensions = wrf_nc_infile.dimensions.keys()
    for dim in dimensions:
        _copy_dimension(wrf_nc_infile, wrf_nc_outfile, dim) 
    ## close the files and garbage collect
    wrf_nc_infile.close()
    wrf_nc_outfile.close()
    gc.collect()

def copy_dimension(wrf_infile, wrf_outfile, dim):
    """
    Copy a single dimension from a WRF input file
    over to a WRF output file.
    """
    ## open the files
    wrf_nc_infile = wrfopen(wrf_infile)
    wrf_nc_outfile = wrfopen(wrf_outfile, mode="a", ncformat=wrf_nc_infile.data_model)
    ## copy the dimension
    _copy_dimension(wrf_nc_infile, wrf_nc_outfile, dim)
    ## close the files and garbage collect
    wrf_nc_infile.close()
    wrf_nc_outfile.close()
    gc.collect()

def _copy_dimension(wrf_nc_infile, wrf_nc_outfile, dim):
    """
    Copy a dimension from a given, open wrf input and
    output netCDF file. Does not open or close file.
    See copy_dimension or copy_all_dimensions, as they
    are wrappers around this function.
    """
    wrf_nc_outfile.createDimension(dim, len(wrf_nc_infile.dimensions[dim]))

def copy_attributes(wrf_infile, wrf_outfile):
    """
    Copyt the netCDF attributes from an input wrf file
    top an output wrf file. wrf_infile and wrf_outfile
    are assumed to be strings containing the paths to 
    existing input and output files.
    """
    ## open the files
    wrf_nc_infile = wrfopen(wrf_infile)
    wrf_nc_outfile = wrfopen(wrf_outfile, mode="a", ncformat=wrf_nc_infile.data_model)
    ## get the list of attributes in the input file,
    ## then loop over them and create a corresponding 
    ## attribute in the output file
    attrs = wrf_nc_infile.ncattrs()
    for attr in attrs:
        wrf_nc_outfile.setncattr( attr, wrf_nc_infile.getncattr( attr ) )
    ## close the files and garbage collect
    wrf_nc_infile.close()
    wrf_nc_outfile.close()
    gc.collect()

def copy_all_variables(wrf_infile, wrf_outfile):
    """
    Take all variables in the WRF input file and copy
    them to the WRF output file.
    """ 
    ## open the files and get the
    ## list of available variables
    wrf_nc_infile = wrfopen(wrf_infile)
    wrf_nc_outfile = wrfopen(wrf_outfile, mode="a", ncformat=wrf_nc_infile.data_model)
    variables = wrf_nc_infile.variables.keys()
    ## loop over every variable and call the _copy_variable
    ## function in this package
    for var in variables:
        _copy_variable(wrf_nc_infile, wrf_nc_outfile, var)
    ## close the files and garbage collect
    wrf_nc_infile.close()
    wrf_nc_outfile.close()
    gc.collect()

def copy_variable(wrf_infile, wrf_outfile, variable):
    """
    Take a single variable from the WRF input file
    and copy it to the WRF output file.
    """
    ## open the files
    wrf_nc_infile = wrfopen(wrf_infile)
    wrf_nc_outfile = wrfopen(wrf_outfile, mode="a", ncformat=wrf_nc_infile.data_model)
    ## copy the variable
    _copy_variable(wrf_nc_infile, wrf_nc_outfile, variable)
    ## close the files and garbage collect
    wrf_nc_infile.close()
    wrf_nc_outfile.close()
    gc.collect()

def _copy_variable(wrf_nc_infile, wrf_nc_outfile, variable):
    """
    Copy a variable from a given, open wrf input and
    output netCDF file. Does not open or close the file.
    See copy_variable or copy_all_variables, as they
    are wrappers around this function.
    """
    ## get the variable object from the ncfile
    var = wrf_nc_infile.variables[variable]
    ## create a new variale in the output file using the information
    ## from the input file, and then copy the data values over
    wrf_nc_outfile.createVariable(variable, var.datatype, var.dimensions)
    for attr in var.ncattrs():
        wrf_nc_outfile.variables[variable].setncattr(attr, var.getncattr(attr))
    wrf_nc_outfile.variables[variable][:] = var[:]
    ## delete the variable from memory for efficiency purposes
    del var

def write_all_variables(wrf_outfile, var_names, data_arrs, dims=None, attr_dict={}):
    """
    Given an output file, a list of variable names, a list of data
    arrays corresponding to those names, and a list of tuple dimensions,
    write out the variables to the output netCDF file.

    Optionally, if you wish to provide the variable with attributes,
    a dictionary of attribute names and their values may be specified via
    attr_dict.
    """
    if dims == None:
        print "Dimension cannot be None. Aborting..."
        return
    ## open the file for append writing
    wrf_nc_outfile = wrfopen(wrf_outfile, mode="a")
    ## loop over the provided variable names, data, and dimensions
    ## and write the variables to the netcdf file
    for var_name, data_arr, dim in zip(var_names, data_arrs, dims):
        _write_variable(wrf_nc_outfile, var_name, data_arr, dim)
    ## close the file and garbage collect
    wrf_nc_outfile.close()
    gc.collect()

def write_variable(wrf_outfile, var_name, data_arr, dims=None, attr_dict={}):
    """
    Write out a new variable.
    Requires a path to the output file, the string name of the
    variable, the data array, and the tuple of string dimension
    names corresponding to the dimensions of the data array.
    
    Optionally, if you wish to provide the variable with attributes,
    a dictionary of attribute names and their values may be specified via
    attr_dict.
    """
    if dims == None:
        print "Dimension cannot be None. Aborting..."
        return
    ## open the file for append writing
    wrf_nc_outfile = wrfopen(wrf_outfile, mode="a")
    ## write the variable
    _write_variable(wrf_nc_file, var_name, data_arr, dims=dims)
    ## close the file and garbage collect
    wrf_nc_outfile.close()
    gc.collect()

def _write_variable(wrf_nc_outfile, var_name, data_arr, dims=None, attr_dict={}):
    """
    Handles creating and writing a new variable to the WRF output
    file. Not to be called stand alone. See write_variable for usage,
    as it is a wrapper around this function.
    """
    wrf_nc_outfile.createVariable(var_name, data_arr.dtype, dims)
    wrf_nc_outfile.variables[var_name].setncatts(attr_dict)
