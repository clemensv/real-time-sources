<#
.SYNOPSIS
    This script generates event markdown files.

.DESCRIPTION
    The script is designed to automate the generation of markdown files for events.
    It should be executed from the specified directory to ensure all dependencies and resources are correctly referenced.

.PARAMETER None
    No parameters are required for this script.

.EXAMPLE
    To run this script, navigate to the directory using pushd and execute the script.

.NOTES
    Author: [Your Name]
    Date: [Date]
    FilePath: /c:/git/real-time-sources/tools/generate-events-md.ps1
#>

pushd $PSScriptRoot

python .\printdoc.py ..\gtfs\xreg\gtfs.xreg.json --title "GTFS API Bridge Events" --description "This document describes the events that are emitted by the GTFS API Bridge." --output ..\gtfs\EVENTS.md
python .\printdoc.py ..\pegelonline\xreg\pegelonline.xreg.json --title "PegelOnline API Bridge Events" --description "This document describes the events that are emitted by the PegelOnline API Bridge." --output ..\pegelonline\EVENTS.md
python .\printdoc.py ..\rss\xreg\feeds.xreg.json --title "RSS API Bridge Events" --description "This document describes the events that are emitted by the RSS API Bridge." --output ..\rss\EVENTS.md
python .\printdoc.py ..\noaa\xreg\noaa.xreg.json --title "NOAA Tides and Currents API Bridge Events" --description "This document describes the events that are emitted by the NOAA API Bridge." --output ..\noaa\EVENTS.md
python .\printdoc.py ..\noaa-ndbc\xreg\noaa_ndbc.xreg.json --title "NOAA NDBC Buoy Observations Bridge Events" --description "This document describes the events emitted by the NOAA NDBC Buoy Observations bridge." --output ..\noaa-ndbc\EVENTS.md
python .\printdoc.py ..\usgs-iv\xreg\usgs_iv.xreg.json --title "USGS Instantaneous Values API Bridge Events" --description "This document describes the events that are emitted by the USGS Instantaneous Values API Bridge." --output ..\usgs-iv\EVENTS.md
python .\printdoc.py ..\mode-s\xreg\mode_s.xreg.json --title "Mode-S API Bridge Events" --description "This document describes the events that are emitted by the Mode-S API Bridge." --output ..\mode-s\EVENTS.md
python .\printdoc.py ..\dwd\xreg\dwd.xreg.json --title "DWD Open Data Bridge Events" --description "This document describes the events emitted by the DWD Open Data bridge." --output ..\dwd\EVENTS.md
python .\printdoc.py ..\digitraffic-maritime\xreg\digitraffic_maritime.xreg.json --title "Digitraffic Marine Bridge Events" --description "This document describes the events emitted by the Digitraffic Marine bridge." --output ..\digitraffic-maritime\EVENTS.md
python .\printdoc.py ..\kystverket-ais\xreg\ais.xreg.json --title "Kystverket AIS Bridge Events" --description "This document describes the events emitted by the Kystverket AIS bridge." --output ..\kystverket-ais\EVENTS.md
python .\printdoc.py ..\entsoe\xreg\entsoe.xreg.json --title "ENTSO-E Transparency Platform Bridge Events" --description "This document describes the events that are emitted by the ENTSO-E Transparency Platform Bridge." --output ..\entsoe\EVENTS.md
python .\printdoc.py ..\laqn-london\xreg\laqn_london.xreg.json --title "LAQN London Air Quality Network Bridge Events" --description "This document describes the events emitted by the LAQN London Air Quality Network bridge." --output ..\laqn-london\EVENTS.md
python .\printdoc.py ..\uba-airdata\xreg\uba_airdata.xreg.json --title "UBA Germany Air Quality Bridge Events" --description "This document describes the events emitted by the UBA Germany Air Quality bridge." --output ..\uba-airdata\EVENTS.md

popd
