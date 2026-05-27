.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./tepco_denkiyoho_mqtt_producer_data ./tepco_denkiyoho_mqtt_producer_mqtt_client

install: build
	cd tepco_denkiyoho_mqtt_producer_data && poetry install
	cd tepco_denkiyoho_mqtt_producer_mqtt_client && poetry install
	pip install ./tepco_denkiyoho_mqtt_producer_data ./tepco_denkiyoho_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./tepco_denkiyoho_mqtt_producer_mqtt_client/tests ./tepco_denkiyoho_mqtt_producer_data/tests