.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./ticketmaster_mqtt_producer_data ./ticketmaster_mqtt_producer_mqtt_client

install: build
	cd ticketmaster_mqtt_producer_data && poetry install
	cd ticketmaster_mqtt_producer_mqtt_client && poetry install
	pip install ./ticketmaster_mqtt_producer_data ./ticketmaster_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./ticketmaster_mqtt_producer_mqtt_client/tests ./ticketmaster_mqtt_producer_data/tests