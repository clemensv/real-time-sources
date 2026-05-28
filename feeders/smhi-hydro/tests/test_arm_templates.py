import json
from pathlib import Path


SOURCE_DIR = Path(__file__).resolve().parents[1]


def test_smhi_hydro_mqtt_arm_templates_exist_and_are_valid_json():
    template_paths = [
        SOURCE_DIR / "azure-template-mqtt.json",
        SOURCE_DIR / "azure-template-with-eventgrid-mqtt.json",
    ]

    for template_path in template_paths:
        data = json.loads(template_path.read_text(encoding="utf-8"))
        assert data["$schema"].endswith("deploymentTemplate.json#")
        assert isinstance(data["resources"], list)


def test_smhi_hydro_mqtt_arm_templates_target_the_mqtt_image():
    byo = json.loads((SOURCE_DIR / "azure-template-mqtt.json").read_text(encoding="utf-8"))
    eventgrid = json.loads((SOURCE_DIR / "azure-template-with-eventgrid-mqtt.json").read_text(encoding="utf-8"))

    assert byo["parameters"]["imageName"]["defaultValue"] == "ghcr.io/clemensv/real-time-sources-smhi-hydro-mqtt:latest"
    assert eventgrid["parameters"]["imageName"]["defaultValue"] == "ghcr.io/clemensv/real-time-sources-smhi-hydro-mqtt:latest"
