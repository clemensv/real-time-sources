# __init.py__
from . import gtfs_cli
from ._version import __version__

if __name__ == "__main__":
    gtfs_cli.main()
