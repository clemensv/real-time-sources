.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./irceline_belgium_mqtt_producer_data ./irceline_belgium_mqtt_producer_mqtt_client

install: build
	cd irceline_belgium_mqtt_producer_data && poetry install
	cd irceline_belgium_mqtt_producer_mqtt_client && poetry install
	pip install ./irceline_belgium_mqtt_producer_data ./irceline_belgium_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./irceline_belgium_mqtt_producer_mqtt_client/tests ./irceline_belgium_mqtt_producer_data/tests