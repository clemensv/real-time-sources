.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./noaa_amqp_producer_data ./noaa_amqp_producer_amqp_producer

install: build
	cd noaa_amqp_producer_data && poetry install
	cd noaa_amqp_producer_amqp_producer && poetry install
	pip install ./noaa_amqp_producer_data ./noaa_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./noaa_amqp_producer_amqp_producer/tests ./noaa_amqp_producer_data/tests
