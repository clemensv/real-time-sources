.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./inpe_deter_brazil_mqtt_producer_data ./inpe_deter_brazil_mqtt_producer_mqtt_client

install: build
	cd inpe_deter_brazil_mqtt_producer_data && poetry install
	cd inpe_deter_brazil_mqtt_producer_mqtt_client && poetry install
	pip install ./inpe_deter_brazil_mqtt_producer_data ./inpe_deter_brazil_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./inpe_deter_brazil_mqtt_producer_mqtt_client/tests ./inpe_deter_brazil_mqtt_producer_data/tests