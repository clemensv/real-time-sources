.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./noaa-nws-producer_data ./noaa-nws-producer_kafka_producer

install: build
	cd noaa-nws-producer_data && poetry install
	cd noaa-nws-producer_kafka_producer && poetry install
	pip install ./noaa-nws-producer_data ./noaa-nws-producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./noaa-nws-producer_kafka_producer/tests ./noaa-nws-producer_data/tests