import json
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[1]


def _load_template(name: str) -> dict:
    return json.loads((SOURCE_ROOT / name).read_text(encoding="utf-8"))


def _container_env(template: dict) -> dict:
    container_group = next(
        resource
        for resource in template["resources"]
        if resource["type"] == "Microsoft.ContainerInstance/containerGroups"
    )
    variables = container_group["properties"]["containers"][0]["properties"]["environmentVariables"]
    return {variable["name"]: variable for variable in variables}


class TestAzureMqttTemplates:
    def test_byo_mqtt_template_wires_required_inputs(self):
        template = _load_template("azure-template-mqtt.json")

        assert template["parameters"]["brokerUrl"]["type"] == "string"
        assert template["parameters"]["imageName"]["defaultValue"] == (
            "ghcr.io/clemensv/real-time-sources-aisstream-mqtt:latest"
        )

        env = _container_env(template)
        assert env["MQTT_BROKER_URL"]["value"] == "[parameters('brokerUrl')]"
        assert env["AISSTREAM_API_KEY"]["secureValue"] == "[parameters('aisstreamApiKey')]"
        assert env["AISSTREAM_BOUNDING_BOXES"]["value"] == "[parameters('aisstreamBoundingBoxes')]"

    def test_eventgrid_template_uses_aisstream_topic_root_and_entra(self):
        template = _load_template("azure-template-with-eventgrid-mqtt.json")

        assert template["parameters"]["topicRoot"]["defaultValue"] == "maritime/intl/aisstream/aisstream/#"

        env = _container_env(template)
        assert env["MQTT_AUTH_MODE"]["value"] == "entra"
        assert env["MQTT_ENTRA_AUDIENCE"]["value"] == "https://eventgrid.azure.net/"
        assert "topicSpacesConfiguration.hostname" in env["MQTT_BROKER_URL"]["value"]
