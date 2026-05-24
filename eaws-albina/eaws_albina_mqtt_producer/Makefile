.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./eaws_albina_mqtt_producer_data ./eaws_albina_mqtt_producer_mqtt_client

install: build
	cd eaws_albina_mqtt_producer_data && poetry install
	cd eaws_albina_mqtt_producer_mqtt_client && poetry install
	pip install ./eaws_albina_mqtt_producer_data ./eaws_albina_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./eaws_albina_mqtt_producer_mqtt_client/tests ./eaws_albina_mqtt_producer_data/tests