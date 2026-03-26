.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./noaa-goes-producer_data ./noaa-goes-producer_kafka_producer

install: build
	cd noaa-goes-producer_data && poetry install
	cd noaa-goes-producer_kafka_producer && poetry install
	pip install ./noaa-goes-producer_data ./noaa-goes-producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./noaa-goes-producer_kafka_producer/tests ./noaa-goes-producer_data/tests