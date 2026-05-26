.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./uk_ea_flood_monitoring_mqtt_producer_data ./uk_ea_flood_monitoring_mqtt_producer_mqtt_client

install: build
	cd uk_ea_flood_monitoring_mqtt_producer_data && poetry install
	cd uk_ea_flood_monitoring_mqtt_producer_mqtt_client && poetry install
	pip install ./uk_ea_flood_monitoring_mqtt_producer_data ./uk_ea_flood_monitoring_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./uk_ea_flood_monitoring_mqtt_producer_mqtt_client/tests ./uk_ea_flood_monitoring_mqtt_producer_data/tests