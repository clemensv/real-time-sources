"""Compatibility shim for the local noaa_core package layout.

When the feeder runs from its source tree (or the container ``/app`` working
directory), the project directory ``noaa_core`` would otherwise shadow the
installed ``noaa_core`` package as a namespace package. This shim turns the
project directory into a regular package that simply re-exports the real
implementation from the nested ``noaa_core`` package.
"""

from .noaa_core import *  # noqa: F401,F403
from .noaa_core import (  # noqa: F401
    NOAAClient,
    PRODUCT_ORDER,
    SOURCE_URI,
    STATIONS_URL,
    USER_AGENT,
    VISIBILITY_DATACONTENTTYPE,
    VISIBILITY_DATASCHEMA,
    default_last_polled_file,
    extract_fields,
    load_last_polled_times,
    record_timestamp,
    save_last_polled_times,
    select_stations,
)
