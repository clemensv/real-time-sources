.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./paris_bicycle_counters_mqtt_producer_data ./paris_bicycle_counters_mqtt_producer_mqtt_client

install: build
	cd paris_bicycle_counters_mqtt_producer_data && poetry install
	cd paris_bicycle_counters_mqtt_producer_mqtt_client && poetry install
	pip install ./paris_bicycle_counters_mqtt_producer_data ./paris_bicycle_counters_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./paris_bicycle_counters_mqtt_producer_mqtt_client/tests ./paris_bicycle_counters_mqtt_producer_data/tests