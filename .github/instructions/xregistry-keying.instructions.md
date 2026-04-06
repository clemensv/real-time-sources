---
applyTo: "**/xreg/*.xreg.json"
---

When editing xRegistry manifests for this repo:

- Every CloudEvents message must declare a `subject` metadata entry with `type: "uritemplate"`.
- Every Kafka producer endpoint must declare `protocoloptions.options.key`, and that key template must match the message `subject` template exactly.
- Choose keys from stable domain identity fields such as station identifiers, MMSI, alert IDs, or timeseries identifiers. Do not use descriptive labels or other mutable fields as Kafka keys.
- If messages in the same producer use materially different identity shapes, split them into separate `messagegroups` and Kafka endpoints instead of forcing one shared key model.
- Multi-part identities should stay aligned between `subject` and endpoint `key`, for example `{agency_cd}/{site_no}` or `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`.
- After changing key or subject modeling, regenerate the affected producers with `xrcg` `0.10.1` so the generated Kafka producers and tests pick up the current default key behavior.
