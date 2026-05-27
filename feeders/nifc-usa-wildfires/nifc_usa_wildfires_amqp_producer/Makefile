.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./nifc_usa_wildfires_amqp_producer_data ./nifc_usa_wildfires_amqp_producer_amqp_producer

install: build
	cd nifc_usa_wildfires_amqp_producer_data && poetry install
	cd nifc_usa_wildfires_amqp_producer_amqp_producer && poetry install
	pip install ./nifc_usa_wildfires_amqp_producer_data ./nifc_usa_wildfires_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./nifc_usa_wildfires_amqp_producer_amqp_producer/tests ./nifc_usa_wildfires_amqp_producer_data/tests
