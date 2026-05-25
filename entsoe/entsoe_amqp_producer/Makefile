.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./entsoe_amqp_producer_data ./entsoe_amqp_producer_amqp_producer

install: build
	cd entsoe_amqp_producer_data && poetry install
	cd entsoe_amqp_producer_amqp_producer && poetry install
	pip install ./entsoe_amqp_producer_data ./entsoe_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./entsoe_amqp_producer_amqp_producer/tests ./entsoe_amqp_producer_data/tests
