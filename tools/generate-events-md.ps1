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

python .\printdoc.py ..\gtfs\xreg\gtfs.xreg.json --title "GTFS API Bridge Events" --description "This document describes the events that are emitted by the GTFS API Bridge." > ..\gtfs\EVENTS.md
python .\printdoc.py ..\pegelonline\xreg\pegelonline.xreg.json --title "PegelOnline API Bridge Events" --description "This document describes the events that are emitted by the PegelOnline API Bridge." > ..\pegelonline\EVENTS.md
python .\printdoc.py ..\rss\xreg\feeds.xreg.json --title "RSS API Bridge Events" --description "This document describes the events that are emitted by the RSS API Bridge." > ..\rss\EVENTS.md
python .\printdoc.py ..\noaa\xreg\noaa.xreg.json --title "NOAA Tides and Currents API Bridge Events" --description "This document describes the events that are emitted by the NOAA API Bridge." > ..\noaa\EVENTS.md
python .\printdoc.py ..\usgs-iv\xreg\usgs_iv.xreg.json --title "USGS Instantaneous Values API Bridge Events" --description "This document describes the events that are emitted by the USGS Instantaneous Values API Bridge." > ..\usgs-iv\EVENTS.md
python .\printdoc.py ..\mode-s\xreg\mode_s.xreg.json --title "Mode-S API Bridge Events" --description "This document describes the events that are emitted by the Mode-S API Bridge." > ..\mode-s\EVENTS.md

popd