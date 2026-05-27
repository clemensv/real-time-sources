.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./cbp_border_wait_mqtt_producer_data ./cbp_border_wait_mqtt_producer_mqtt_client

install: build
	cd cbp_border_wait_mqtt_producer_data && poetry install
	cd cbp_border_wait_mqtt_producer_mqtt_client && poetry install
	pip install ./cbp_border_wait_mqtt_producer_data ./cbp_border_wait_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./cbp_border_wait_mqtt_producer_mqtt_client/tests ./cbp_border_wait_mqtt_producer_data/tests