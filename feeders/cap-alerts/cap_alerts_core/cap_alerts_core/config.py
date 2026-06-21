from __future__ import annotations

def parse_bool(value, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def parse_kafka_connection_string(connection_string: str) -> dict[str, str]:
    cfg = {
        "security.protocol": "SASL_SSL",
        "sasl.mechanisms": "PLAIN",
        "sasl.username": "$ConnectionString",
        "sasl.password": connection_string.strip(),
    }
    for part in connection_string.split(";"):
        if part.startswith("Endpoint="):
            cfg["bootstrap.servers"] = part.split("=", 1)[1].strip('"').replace("sb://", "").rstrip("/") + ":9093"
        elif part.startswith("BootstrapServer="):
            cfg["bootstrap.servers"] = part.split("=", 1)[1].strip('"')
            cfg["security.protocol"] = "PLAINTEXT"
            cfg.pop("sasl.mechanisms", None); cfg.pop("sasl.username", None); cfg.pop("sasl.password", None)
        elif part.startswith("EntityPath="):
            cfg["kafka_topic"] = part.split("=", 1)[1].strip('"')
    return cfg


def build_kafka_config(*, bootstrap_servers: str, sasl_username: str | None, sasl_password: str | None, tls_enabled: bool = True) -> dict[str, str]:
    cfg = {"bootstrap.servers": bootstrap_servers, "security.protocol": "SASL_SSL" if tls_enabled else "PLAINTEXT"}
    if sasl_username and sasl_password:
        cfg.update({"sasl.mechanisms": "PLAIN", "sasl.username": sasl_username, "sasl.password": sasl_password})
    return cfg
