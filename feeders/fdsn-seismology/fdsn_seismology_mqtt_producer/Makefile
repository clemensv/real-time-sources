.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./fdsn_seismology_mqtt_producer_data ./fdsn_seismology_mqtt_producer_mqtt_client

install: build
	cd fdsn_seismology_mqtt_producer_data && poetry install
	cd fdsn_seismology_mqtt_producer_mqtt_client && poetry install
	pip install ./fdsn_seismology_mqtt_producer_data ./fdsn_seismology_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./fdsn_seismology_mqtt_producer_mqtt_client/tests ./fdsn_seismology_mqtt_producer_data/tests