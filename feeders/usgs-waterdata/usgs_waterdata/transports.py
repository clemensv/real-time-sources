"""Generated producer adapters; acknowledgement checks remain outside generated files."""

from __future__ import annotations

import asyncio
import copy
import dataclasses
from datetime import datetime, timedelta
from functools import lru_cache
import importlib
import os
import re
import types
import typing
from typing import Any, SupportsIndex
from urllib.parse import unquote, urlsplit

from usgs_waterdata_core.delivery import AcknowledgedKafkaProducer, fabric_kafka_config

from .app import boolean

LEAVES = {"ContinuousObservation": "continuous_observation", "MonitoringLocation": "monitoring_location",
          "TimeSeries": "time_series", "Parameter": "parameter"}


class ExactDateTime(datetime):
    """Keep the original RFC3339 spelling when serializing precision beyond microseconds."""

    original_text: str

    @classmethod
    def from_text(cls, value: str) -> ExactDateTime:
        # Python 3.10 accepts only three/six fractional digits; wire text remains authoritative.
        normalized = re.sub(r"(\d{2}:\d{2}:\d{2})\.(\d+)",
                            lambda match: match[1] + "." + match[2][:6].ljust(6, "0"),
                            value.replace("Z", "+00:00"))
        parsed = datetime.fromisoformat(normalized)
        result = cls(parsed.year, parsed.month, parsed.day, parsed.hour, parsed.minute, parsed.second,
                     parsed.microsecond, tzinfo=parsed.tzinfo, fold=parsed.fold)
        result.original_text = value
        return result

    def isoformat(self, sep: str = "T", timespec: str = "auto") -> str:
        return self.original_text

    def __reduce_ex__(self, protocol: SupportsIndex) -> Any:
        return (type(self).from_text, (self.original_text,))


@lru_cache
def duration_record(cls: Any) -> Any:
    # WORKAROUND(https://github.com/clemensv/avrotize/issues/572): retain a typed duration, encode its original text.
    def to_json(instance, *args, **kwargs):
        serializable = copy.copy(instance)
        serializable.data_gap_interval = instance._duration_text
        return cls.to_json(serializable, *args, **kwargs)

    return type(f"DurationWire{cls.__name__}", (cls,), {"to_json": to_json})


def model_instance(cls: Any, payload: dict[str, Any]) -> Any:
    """Construct nested generated classes and parse their declared Python primitive types."""
    hints = typing.get_type_hints(cls)

    def convert(kind: Any, value: Any) -> Any:
        if value is None:
            return None
        origin = typing.get_origin(kind)
        if origin in (typing.Union, types.UnionType):
            kind = next(t for t in typing.get_args(kind) if t is not type(None))
            return convert(kind, value)
        if origin is list:
            return [convert(typing.get_args(kind)[0], item) for item in value]
        if dataclasses.is_dataclass(kind):
            return model_instance(kind, value)
        if kind is datetime:
            return ExactDateTime.from_text(value)
        if kind is timedelta:
            from isodate import parse_duration
            if not isinstance(value, str):
                raise ValueError("USGS duration must retain its upstream ISO-8601 text")
            return parse_duration(value)
        if kind is float:
            return float(value)
        if kind is int:
            return int(value)
        return value

    fields = dataclasses.fields(cls)
    expected = {f.name.rstrip("_") for f in fields}
    unknown = payload.keys() - expected
    if unknown:
        raise ValueError(f"Unmodeled fields in {cls.__name__}: {sorted(unknown)}")
    values = {f.name: convert(hints[f.name], payload.get(f.name.rstrip("_"))) for f in fields}
    duration_text = payload.get("data_gap_interval")
    if duration_text is not None:
        instance = duration_record(cls)(**values)
        instance._duration_text = duration_text
        return instance
    return cls(**values)


def generated(transport: str) -> tuple[Any, dict[str, Any]]:
    stem = "usgs_waterdata_producer" if transport == "kafka" else f"usgs_waterdata_{transport}_producer"
    suffix, module_name = {"kafka": ("kafka_producer", "producer"),
                           "mqtt": ("mqtt_client", "client"), "amqp": ("amqp_producer", "producer")}[transport]
    module = importlib.import_module(f"{stem}_{suffix}.{module_name}")
    matches = [
        value for name, value in vars(module).items()
        if isinstance(value, type) and value.__module__ == module.__name__
        and (name.endswith("EventProducer") if transport == "kafka" else
             name.endswith("MqttClient") if transport == "mqtt" else name.endswith("AmqpProducer"))
    ]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one generated {transport} producer; found {len(matches)}")
    data = importlib.import_module(f"{stem}_data")
    return matches[0], {family: getattr(data, family) for family in LEAVES}


class KafkaSink:
    def __init__(self) -> None:
        from confluent_kafka import Producer

        cls, self.models = generated("kafka")
        connection = os.getenv("CONNECTION_STRING", "")
        topic = os.getenv("KAFKA_TOPIC", "usgs-waterdata")
        if connection:
            parts = {key.lower(): value for item in connection.split(";") if "=" in item
                     for key, value in [item.strip().split("=", 1)]}
            if "endpoint" in parts:
                config, entity_topic = cls.parse_connection_string(connection)
                topic = entity_topic or topic
            else:
                bootstrap = next((parts[key] for key in ("bootstrapserver", "bootstrapservers", "bootstrap.servers")
                                  if key in parts), None)
                if not bootstrap:
                    raise ValueError("CONNECTION_STRING needs BootstrapServer or an Event Hubs Endpoint")
                config = {"bootstrap.servers": bootstrap}
                topic = parts.get("entitypath", topic)
        else:
            config = {"bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")}
        tls = boolean(os.getenv("KAFKA_ENABLE_TLS", "true"))
        username, password = os.getenv("SASL_USERNAME"), os.getenv("SASL_PASSWORD")
        if bool(username) != bool(password):
            raise ValueError("SASL_USERNAME and SASL_PASSWORD must be supplied together")
        if username:
            config.update({"sasl.username": username, "sasl.password": password,
                           "sasl.mechanism": os.getenv("SASL_MECHANISM", "PLAIN"),
                           "security.protocol": "SASL_SSL" if tls else "SASL_PLAINTEXT"})
        elif "security.protocol" not in config:
            config["security.protocol"] = "SSL" if tls else "PLAINTEXT"
        self.raw = AcknowledgedKafkaProducer(Producer(fabric_kafka_config(config)))
        self.producer = cls(self.raw, topic, content_mode="structured")

    async def send(self, family: str, series_id: str, payload: dict[str, Any]) -> None:
        method = getattr(self.producer, f"send_usgs_water_data_kafka_{LEAVES[family]}")
        method(_time_series_id=series_id, data=model_instance(self.models[family], payload),
               _time=payload.get("time"), flush_producer=False)

    async def flush(self) -> None:
        self.raw.poll(0)
        self.raw.flush(timeout=120)

    async def close(self) -> None:
        await self.flush()


class MqttSink:
    async def start(self) -> None:
        import paho.mqtt.client as mqtt
        cls, self.models = generated("mqtt")
        self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5,
                                  client_id=os.getenv("MQTT_CLIENT_ID", "usgs-waterdata"))
        self.producer = cls(self.client, content_mode="binary")
        url = os.environ["MQTT_BROKER_URL"]
        parsed = urlsplit(url if "://" in url else f"mqtt://{url}")
        if not parsed.hostname:
            raise ValueError("MQTT_BROKER_URL needs a hostname")
        self.host = parsed.hostname
        tls = boolean(os.getenv("MQTT_ENABLE_TLS", "false" if "://" in url and parsed.scheme == "mqtt" else "true"))
        self.port = parsed.port or (8883 if tls else 1883)
        mode = os.getenv("MQTT_AUTH_MODE", "anonymous")
        if mode not in {"anonymous", "userpass", "password", "tls-cert", "entra"}:
            raise ValueError("Unsupported MQTT_AUTH_MODE")
        if mode in {"userpass", "password"}:
            username, password = os.getenv("MQTT_USERNAME"), os.getenv("MQTT_PASSWORD")
            if not username or not password:
                raise ValueError("MQTT userpass authentication requires MQTT_USERNAME and MQTT_PASSWORD")
            self.client.username_pw_set(username, password)
        elif mode == "entra" and os.getenv("MQTT_USERNAME"):
            self.client.username_pw_set(os.environ["MQTT_USERNAME"])
        if mode in {"entra", "tls-cert"} and not tls:
            raise ValueError("MQTT Entra/certificate authentication requires TLS")
        if mode == "tls-cert" and not (os.getenv("MQTT_CLIENT_CERT") and os.getenv("MQTT_CLIENT_KEY")):
            raise ValueError("MQTT certificate authentication requires MQTT_CLIENT_CERT and MQTT_CLIENT_KEY")
        if tls:
            self.client.tls_set(ca_certs=os.getenv("MQTT_CA_FILE") or None,
                                certfile=os.getenv("MQTT_CLIENT_CERT") if mode == "tls-cert" else None,
                                keyfile=os.getenv("MQTT_CLIENT_KEY") if mode == "tls-cert" else None)
        self.pending: list[Any] = []
        self.errors: list[str] = []
        publish = self.client.publish

        def acknowledged(client, userdata, mid, reason_code, properties):
            if getattr(reason_code, "is_failure", False):
                self.errors.append(str(reason_code))

        self.client.on_publish = acknowledged

        def tracked(*args, **kwargs):
            receipt = publish(*args, **kwargs)
            if receipt.rc != mqtt.MQTT_ERR_SUCCESS:
                raise RuntimeError(f"MQTT publish enqueue failed: {receipt.rc}")
            self.pending.append(receipt)
            return receipt

        self.client.publish = tracked
        self.credential = None
        self.refresh_task = None
        if mode == "entra":
            from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
            client_id = os.getenv("MQTT_ENTRA_CLIENT_ID")
            self.credential = ManagedIdentityCredential(client_id=client_id) if client_id else DefaultAzureCredential()
            audience = os.getenv("MQTT_ENTRA_AUDIENCE", "https://eventgrid.azure.net/")
            scope = audience.rstrip("/") + "/.default" if not audience.endswith("/.default") else audience
            token = self.credential.get_token(scope)
            await self.producer.connect(self.host, self.port, token=token.token)

            async def refresh():
                nonlocal token
                import time
                while True:
                    await asyncio.sleep(max(30, token.expires_on - time.time() - 300))
                    await self.flush()
                    token = self.credential.get_token(scope)
                    await self.producer.disconnect()
                    await self.producer.connect(self.host, self.port, token=token.token)

            self.refresh_task = asyncio.create_task(refresh())
        else:
            await self.producer.connect(self.host, self.port)

    async def send(self, family: str, series_id: str, payload: dict[str, Any]) -> None:
        if self.refresh_task and self.refresh_task.done():
            self.refresh_task.result()
        method = getattr(self.producer, f"publish_usgs_water_data_mqtt_{LEAVES[family]}")
        await method(time_series_id=series_id, data=model_instance(self.models[family], payload),
                     _time=payload.get("time"))

    async def flush(self) -> None:
        receipts, self.pending = self.pending, []
        for receipt in receipts:
            await asyncio.to_thread(receipt.wait_for_publish, timeout=120)
            if not receipt.is_published():
                raise RuntimeError("MQTT broker did not acknowledge a QoS-1 publication")
        if self.errors:
            errors, self.errors = self.errors, []
            raise RuntimeError(f"MQTT broker rejected publication: {errors}")

    async def close(self) -> None:
        try:
            await self.flush()
        finally:
            if self.refresh_task:
                self.refresh_task.cancel()
                await asyncio.gather(self.refresh_task, return_exceptions=True)
            await self.producer.disconnect()
            if self.credential:
                self.credential.close()


class AmqpSink:
    def __init__(self) -> None:
        cls, self.models = generated("amqp")
        from proton.reactor import AtLeastOnce
        from proton.utils import BlockingConnection

        # WORKAROUND(https://github.com/xregistry/codegen/issues/699): require remote acceptance and honor password-link TLS.
        def acknowledged_sender(producer):
            producer._blocking_sender_is_presettled = False
            url = producer._build_connection_url()
            if producer._use_tls:
                url = url.replace("amqp://", "amqps://", 1)
            options: dict[str, Any] = {"timeout": 120}
            if producer.username and producer.password:
                options.update(user=producer.username, password=producer.password, sasl_enabled=True,
                               allowed_mechs="PLAIN", allow_insecure_mechs=not producer._use_tls)
            producer._connection = BlockingConnection(url, **options)
            producer._sender = producer._connection.create_sender(producer.address, options=AtLeastOnce())

        acknowledged_producer = type("AcknowledgedProducer", (cls,), {"_init_blocking_sender": acknowledged_sender})

        parsed = urlsplit(os.getenv("AMQP_BROKER_URL", ""))
        tls = boolean(os.getenv("AMQP_USE_TLS", os.getenv(
            "AMQP_TLS", "false" if parsed.scheme == "amqp" else "true")))
        host = parsed.hostname or os.getenv("AMQP_HOST", "localhost")
        port = parsed.port or int(os.getenv("AMQP_PORT", "5671" if tls else "5672"))
        mode = os.getenv("AMQP_AUTH_MODE", "password")
        if mode not in {"password", "entra", "sas"}:
            raise ValueError("AMQP_AUTH_MODE must be password, entra or sas")
        kwargs: dict[str, Any] = {
            "host": host, "port": port, "address": parsed.path.lstrip("/") or os.getenv("AMQP_ADDRESS", "usgs-waterdata"),
            "use_tls": tls, "content_mode": os.getenv("AMQP_CONTENT_MODE", "binary"),
        }
        self.credential = None
        if mode == "entra":
            if not tls:
                raise ValueError("AMQP Entra authentication requires TLS")
            from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
            client_id = os.getenv("AMQP_ENTRA_CLIENT_ID")
            self.credential = ManagedIdentityCredential(client_id=client_id) if client_id else DefaultAzureCredential()
            kwargs.update(credential=self.credential,
                          entra_audience=os.getenv("AMQP_ENTRA_AUDIENCE", "https://servicebus.azure.net/.default"))
        elif mode == "sas":
            kwargs.update(sas_key_name=os.environ["AMQP_SAS_KEY_NAME"], sas_key=os.environ["AMQP_SAS_KEY"])
        else:
            kwargs.update(username=unquote(parsed.username) if parsed.username else os.getenv("AMQP_USERNAME"),
                          password=unquote(parsed.password) if parsed.password else os.getenv("AMQP_PASSWORD"))
            if bool(kwargs["username"]) != bool(kwargs["password"]):
                raise ValueError("AMQP_USERNAME and AMQP_PASSWORD must be supplied together")
        self.producer = acknowledged_producer(**kwargs)

    async def send(self, family: str, series_id: str, payload: dict[str, Any]) -> None:
        method = getattr(self.producer, f"send_{LEAVES[family]}")
        method(_time_series_id=series_id, data=model_instance(self.models[family], payload),
               _time=payload.get("time"))

    async def flush(self) -> None:
        # Generated blocking/reactor sends return only after accepted settlement on these links.
        return None

    async def close(self) -> None:
        self.producer.close()
        if self.credential:
            self.credential.close()


async def open_sink(transport: str) -> Any:
    if transport == "kafka":
        return KafkaSink()
    if transport == "amqp":
        return AmqpSink()
    sink = MqttSink()
    try:
        await sink.start()
    except BaseException:
        try:
            await sink.close()
        except Exception:
            pass
        raise
    return sink
