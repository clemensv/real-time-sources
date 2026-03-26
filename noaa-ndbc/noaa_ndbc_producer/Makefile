.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./noaa-ndbc-producer_data ./noaa-ndbc-producer_kafka_producer

install: build
	cd noaa-ndbc-producer_data && poetry install
	cd noaa-ndbc-producer_kafka_producer && poetry install
	pip install ./noaa-ndbc-producer_data ./noaa-ndbc-producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./noaa-ndbc-producer_kafka_producer/tests ./noaa-ndbc-producer_data/tests