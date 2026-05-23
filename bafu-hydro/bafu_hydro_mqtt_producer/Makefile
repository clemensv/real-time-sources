.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./bafu_hydro_mqtt_producer_data ./bafu_hydro_mqtt_producer_mqtt_client

install: build
	cd bafu_hydro_mqtt_producer_data && poetry install
	cd bafu_hydro_mqtt_producer_mqtt_client && poetry install
	pip install ./bafu_hydro_mqtt_producer_data ./bafu_hydro_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./bafu_hydro_mqtt_producer_mqtt_client/tests ./bafu_hydro_mqtt_producer_data/tests