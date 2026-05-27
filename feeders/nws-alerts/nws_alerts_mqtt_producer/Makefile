.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./nws_alerts_mqtt_producer_data ./nws_alerts_mqtt_producer_mqtt_client

install: build
	cd nws_alerts_mqtt_producer_data && poetry install
	cd nws_alerts_mqtt_producer_mqtt_client && poetry install
	pip install ./nws_alerts_mqtt_producer_data ./nws_alerts_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./nws_alerts_mqtt_producer_mqtt_client/tests ./nws_alerts_mqtt_producer_data/tests