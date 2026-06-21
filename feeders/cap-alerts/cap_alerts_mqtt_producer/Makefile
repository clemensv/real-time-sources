.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./cap_alerts_mqtt_producer_data ./cap_alerts_mqtt_producer_mqtt_client

install: build
	cd cap_alerts_mqtt_producer_data && poetry install
	cd cap_alerts_mqtt_producer_mqtt_client && poetry install
	pip install ./cap_alerts_mqtt_producer_data ./cap_alerts_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./cap_alerts_mqtt_producer_mqtt_client/tests ./cap_alerts_mqtt_producer_data/tests