.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./kmi_belgium_mqtt_producer_data ./kmi_belgium_mqtt_producer_mqtt_client

install: build
	cd kmi_belgium_mqtt_producer_data && poetry install
	cd kmi_belgium_mqtt_producer_mqtt_client && poetry install
	pip install ./kmi_belgium_mqtt_producer_data ./kmi_belgium_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./kmi_belgium_mqtt_producer_mqtt_client/tests ./kmi_belgium_mqtt_producer_data/tests