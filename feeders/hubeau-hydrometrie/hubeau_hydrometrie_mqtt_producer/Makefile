.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./hubeau_hydrometrie_mqtt_producer_data ./hubeau_hydrometrie_mqtt_producer_mqtt_client

install: build
	cd hubeau_hydrometrie_mqtt_producer_data && poetry install
	cd hubeau_hydrometrie_mqtt_producer_mqtt_client && poetry install
	pip install ./hubeau_hydrometrie_mqtt_producer_data ./hubeau_hydrometrie_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./hubeau_hydrometrie_mqtt_producer_mqtt_client/tests ./hubeau_hydrometrie_mqtt_producer_data/tests