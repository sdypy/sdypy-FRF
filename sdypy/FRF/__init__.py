"""sdypy.FRF - frequency response function estimation, re-exported from pyFRF under the sdypy namespace."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("sdypy-FRF")
except PackageNotFoundError:  # source checkout without installed metadata
    __version__ = "0+unknown"

from pyFRF import FRF, assert_sep005, direction_dict

__all__ = ["FRF", "assert_sep005", "direction_dict"]
