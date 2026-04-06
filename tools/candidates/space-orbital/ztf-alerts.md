# ZTF Transient Alert Stream

**Country/Region**: Global
**Publisher**: Zwicky Transient Facility / Caltech
**API Endpoint**: `kafka://public.alerts.ztf.uw.edu:9092` (public mirror at UW)
**Documentation**: https://zwickytransientfacility.github.io/ztf-avro-alert/
**Protocol**: Kafka (Apache Kafka)
**Auth**: None (public mirror); group ID allocation recommended
**Data Format**: Apache Avro (with embedded schemas)
**Update Frequency**: Nightly (alerts generated each observing night)
**License**: Open (public alerts after 2018)

## What It Provides

The Zwicky Transient Facility is a wide-field astronomical survey at Palomar Observatory that scans the sky every 2 days. Each observing night produces hundreds of thousands of transient alerts — supernovae, variable stars, asteroids, active galactic nuclei, and other changing objects. Alerts are distributed via Apache Kafka in Avro format, making ZTF one of the most data-rich real-time astronomy streams.

Each alert packet contains the detection data, a 30-day photometric history, cutout images (science, reference, difference), and cross-match information with known catalogs.

## API Details

- **Public Kafka broker**: `public.alerts.ztf.uw.edu:9092` (University of Washington mirror)
- **Topics**: `ztf_{YYYYMMDD}_programid1` (one topic per night, public program)
- **Message format**: Apache Avro with embedded schema
- **Alert content**: `candid` (candidate ID), `objectId`, `jd` (Julian date), `ra`, `dec`, `magpsf` (magnitude), `sigmapsf`, `fid` (filter ID), `diffmaglim`, `isdiffpos`, `programid`
- **History**: `prv_candidates` — array of previous detections (30-day window)
- **Cutouts**: `cutoutScience`, `cutoutTemplate`, `cutoutDifference` — FITS image stamps (gzip-compressed)
- **Alert rate**: ~100,000-300,000 alerts per observing night
- **Broker services**: ANTARES, ALeRCE, Fink, Lasair provide filtered/classified streams

## Freshness Assessment

Alerts are generated during each observing night at Palomar (weather permitting). Processing pipeline produces alerts within ~10 minutes of image capture. Alerts are distributed via Kafka immediately after processing. There are no alerts during daytime or bad weather. This is a nightly batch stream, not continuous real-time.

## Entity Model

- **Alert**: `candid` (unique candidate ID), detection at a specific time/position
- **Object**: `objectId` (ZTF name, e.g., `ZTF21aaazzzt`), persistent identifier for a sky location
- **Candidate**: Photometric detection with magnitude, position, image quality metrics
- **Previous Candidates**: Historical detections of the same object (light curve history)
- **Cutout**: FITS image stamps centered on the detection

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Nightly batch; ~10 min pipeline latency during observing |
| Openness | 3 | Public Kafka stream, no auth on public mirror |
| Stability | 2 | Active survey (2018-2025+); successor (LSST/Rubin) launching |
| Structure | 3 | Avro with embedded schemas; very well-defined |
| Identifiers | 3 | Persistent ZTF object IDs; unique candidate IDs |
| Additive Value | 3 | Massive real-time astronomical transient stream; Kafka-native |
| **Total** | **16/18** | |

## Notes

- ZTF is a pathfinder for the Vera C. Rubin Observatory (LSST), which will produce 10 million alerts per night starting ~2025.
- Avro format with embedded schemas makes this highly structured and self-describing.
- Kafka-native distribution is unusual and valuable — this is a true streaming data source.
- Alert broker services (ALeRCE, Fink, ANTARES, Lasair) add machine learning classification and filtering.
- Each alert is ~60 KB (with cutout images); full nightly stream is ~6-20 GB.
- Public Kafka mirror at UW requires no credentials but may require group ID coordination for consumer groups.
