.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./australia_wildfires_amqp_producer_data ./australia_wildfires_amqp_producer_amqp_producer

install: build
	cd australia_wildfires_amqp_producer_data && poetry install
	cd australia_wildfires_amqp_producer_amqp_producer && poetry install
	pip install ./australia_wildfires_amqp_producer_data ./australia_wildfires_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./australia_wildfires_amqp_producer_amqp_producer/tests ./australia_wildfires_amqp_producer_data/tests
