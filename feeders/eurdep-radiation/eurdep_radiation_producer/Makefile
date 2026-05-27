.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./eurdep_radiation_producer_data ./eurdep_radiation_producer_kafka_producer

install: build
	cd eurdep_radiation_producer_data && poetry install
	cd eurdep_radiation_producer_kafka_producer && poetry install
	pip install ./eurdep_radiation_producer_data ./eurdep_radiation_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./eurdep_radiation_producer_kafka_producer/tests ./eurdep_radiation_producer_data/tests