.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./gracedb_mqtt_producer_data ./gracedb_mqtt_producer_mqtt_client

install: build
	cd gracedb_mqtt_producer_data && poetry install
	cd gracedb_mqtt_producer_mqtt_client && poetry install
	pip install ./gracedb_mqtt_producer_data ./gracedb_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./gracedb_mqtt_producer_mqtt_client/tests ./gracedb_mqtt_producer_data/tests