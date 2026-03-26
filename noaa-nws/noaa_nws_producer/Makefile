.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./noaa_nws_producer_data ./noaa_nws_producer_kafka_producer

install: build
	cd noaa_nws_producer_data && poetry install
	cd noaa_nws_producer_kafka_producer && poetry install
	pip install ./noaa_nws_producer_data ./noaa_nws_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./noaa_nws_producer_kafka_producer/tests ./noaa_nws_producer_data/tests