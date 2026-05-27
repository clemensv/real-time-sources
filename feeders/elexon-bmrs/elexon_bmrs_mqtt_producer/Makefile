.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./elexon_bmrs_mqtt_producer_data ./elexon_bmrs_mqtt_producer_mqtt_client

install: build
	cd elexon_bmrs_mqtt_producer_data && poetry install
	cd elexon_bmrs_mqtt_producer_mqtt_client && poetry install
	pip install ./elexon_bmrs_mqtt_producer_data ./elexon_bmrs_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./elexon_bmrs_mqtt_producer_mqtt_client/tests ./elexon_bmrs_mqtt_producer_data/tests