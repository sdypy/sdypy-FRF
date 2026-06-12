"""
A project template for the SDyPy effort..
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("sdypy-FRF")
except PackageNotFoundError:  # source checkout without installed metadata
    __version__ = "0+unknown"

from pyFRF import *
