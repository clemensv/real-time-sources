# switch into this directory with pushd
pushd $PSScriptRoot

python .\printdoc.py ..\gtfs\xreg\gtfs.xreg.json --title "GTFS API Bridge Events" --description "This document describes the events that are emitted by the GTFS API Bridge." > ..\gtfs\EVENTS.md
python .\printdoc.py ..\pegelonline\xreg\pegelonline.xreg.json --title "PegelOnline API Bridge Events" --description "This document describes the events that are emitted by the PegelOnline API Bridge." > ..\pegelonline\EVENTS.md
python .\printdoc.py ..\rss\xreg\feeds.xreg.json --title "RSS API Bridge Events" --description "This document describes the events that are emitted by the RSS API Bridge." > ..\rss\EVENTS.md
python .\printdoc.py ..\noaa\noaa\noaa.xreg.json --title "NOAA Tides and Currents API Bridge Events" --description "This document describes the events that are emitted by the NOAA API Bridge." > ..\noaa\EVENTS.md

popd