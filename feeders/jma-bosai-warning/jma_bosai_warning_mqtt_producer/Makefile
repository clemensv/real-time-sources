.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./jma_bosai_warning_mqtt_producer_data ./jma_bosai_warning_mqtt_producer_mqtt_client

install: build
	cd jma_bosai_warning_mqtt_producer_data && poetry install
	cd jma_bosai_warning_mqtt_producer_mqtt_client && poetry install
	pip install ./jma_bosai_warning_mqtt_producer_data ./jma_bosai_warning_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./jma_bosai_warning_mqtt_producer_mqtt_client/tests ./jma_bosai_warning_mqtt_producer_data/tests