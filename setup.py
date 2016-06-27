try:
    from setuptools import setup
    from setuptools import Extension
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension

from Cython.Build import cythonize
import numpy

setup(
    ext_modules = cythonize("RSpectra.pyx"),
    include_dirs = [numpy.get_include()]
)
