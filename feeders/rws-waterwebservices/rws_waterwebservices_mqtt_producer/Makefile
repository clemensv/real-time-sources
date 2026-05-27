.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./rws_waterwebservices_mqtt_producer_data ./rws_waterwebservices_mqtt_producer_mqtt_client

install: build
	cd rws_waterwebservices_mqtt_producer_data && poetry install
	cd rws_waterwebservices_mqtt_producer_mqtt_client && poetry install
	pip install ./rws_waterwebservices_mqtt_producer_data ./rws_waterwebservices_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./rws_waterwebservices_mqtt_producer_mqtt_client/tests ./rws_waterwebservices_mqtt_producer_data/tests