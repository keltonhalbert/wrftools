from numpy.distutils.core import Extension
from numpy.distutils.core import setup


ext1 = Extension(name = "pv_interp",
    sources=["wrftools/src/interp_pv.f90"])

if __name__ == "__main__":
    setup(
          name = "wrftools",
          version = "2.0",
          author = "Kelton Halbert",
          author_email = "keltonhalbert@ou.edu",
          description = ("Functions for post processing WRF data"),
          license = "GPL V2",
          url = "https://github.com/keltonhalbert/wrftools",
          packages=['wrftools'],
          classifiers=["Development Status :: 2 - Beta"],
          ext_modules = [ext1]
          )
