.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./environment_canada_producer_data ./environment_canada_producer_kafka_producer

install: build
	cd environment_canada_producer_data && poetry install
	cd environment_canada_producer_kafka_producer && poetry install
	pip install ./environment_canada_producer_data ./environment_canada_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./environment_canada_producer_kafka_producer/tests ./environment_canada_producer_data/tests