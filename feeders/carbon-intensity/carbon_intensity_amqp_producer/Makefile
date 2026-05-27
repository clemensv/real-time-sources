.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./carbon_intensity_amqp_producer_data ./carbon_intensity_amqp_producer_amqp_producer

install: build
	cd carbon_intensity_amqp_producer_data && poetry install
	cd carbon_intensity_amqp_producer_amqp_producer && poetry install
	pip install ./carbon_intensity_amqp_producer_data ./carbon_intensity_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./carbon_intensity_amqp_producer_amqp_producer/tests ./carbon_intensity_amqp_producer_data/tests
