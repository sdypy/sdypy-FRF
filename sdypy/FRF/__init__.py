"""sdypy.FRF - frequency response function estimation, sdypy namespace entry (code formerly in the pyFRF package)."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("sdypy-FRF")
except PackageNotFoundError:  # source checkout without installed metadata
    __version__ = "0+unknown"

from .frf import FRF, assert_sep005, direction_dict

__all__ = ["FRF", "assert_sep005", "direction_dict"]
