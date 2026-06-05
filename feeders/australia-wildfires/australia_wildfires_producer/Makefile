.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./australia_wildfires_producer_data ./australia_wildfires_producer_kafka_producer

install: build
	cd australia_wildfires_producer_data && poetry install
	cd australia_wildfires_producer_kafka_producer && poetry install
	pip install ./australia_wildfires_producer_data ./australia_wildfires_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./australia_wildfires_producer_kafka_producer/tests ./australia_wildfires_producer_data/tests