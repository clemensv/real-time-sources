# 058 Events MD Generator Checkpoint

## Coverage matrix

| xRegistry surface | Before | After |
| --- | --- | --- |
| Registry name/version/description/documentation | Partial / mostly absent | Rendered in Registry section |
| Endpoint discovery | Hardcoded 13 sources | Repo-driven 102 top-level manifests |
| Kafka endpoint topic/key/messagegroup | Partial | Rendered per endpoint and binding |
| MQTT topic/QoS/retain/alias/clean-start | Missing | Rendered per endpoint/message |
| AMQP address/durable/application properties | Missing | Rendered per endpoint/message |
| Messagegroup description/bindings | Partial | Rendered with endpoint bindings |
| CloudEvents metadata/extensions | Partial | Rendered with type, required, values/templates |
| basemessageurl chains | Partial | Resolved and displayed |
| JsonStructure fields/extensions/validation/defaults | Partial | Rendered for records, enums, nested objects, unions/arrays/choices |
| Avro shape | Basic | Rendered with record fields/enums/ordinals |
| Unknown xreg fields | Silent | Warned to stderr |
| Staleness checking | Missing | `-Check` mode added |

## Results

- Regenerated EVENTS.md files: 102
- Unknown-field warnings from final full generation: 0
- Validation: `python -m unittest discover -s tools\tests -v`; `pwsh tools\generate-events-md.ps1 -Check`
