.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./carbon_intensity_producer_data ./carbon_intensity_producer_kafka_producer

install: build
	cd carbon_intensity_producer_data && poetry install
	cd carbon_intensity_producer_kafka_producer && poetry install
	pip install ./carbon_intensity_producer_data ./carbon_intensity_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./carbon_intensity_producer_kafka_producer/tests ./carbon_intensity_producer_data/tests