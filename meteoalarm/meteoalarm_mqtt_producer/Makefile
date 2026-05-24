.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./meteoalarm_mqtt_producer_data ./meteoalarm_mqtt_producer_mqtt_client

install: build
	cd meteoalarm_mqtt_producer_data && poetry install
	cd meteoalarm_mqtt_producer_mqtt_client && poetry install
	pip install ./meteoalarm_mqtt_producer_data ./meteoalarm_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./meteoalarm_mqtt_producer_mqtt_client/tests ./meteoalarm_mqtt_producer_data/tests