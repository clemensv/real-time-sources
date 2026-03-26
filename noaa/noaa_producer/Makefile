.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./noaa-producer_data ./noaa-producer_kafka_producer

install: build
	cd noaa-producer_data && poetry install
	cd noaa-producer_kafka_producer && poetry install
	pip install ./noaa-producer_data ./noaa-producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./noaa-producer_kafka_producer/tests ./noaa-producer_data/tests