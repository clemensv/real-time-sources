from ._version import version as __version__, version_tuple as __version_tuple__
from .noaa import main

__all__ = ["__version__", "__version_tuple__", "main"]

if __name__ == "__main__":
    main()