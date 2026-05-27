.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./nextbus_amqp_producer_data ./nextbus_amqp_producer_amqp_producer

install: build
	cd nextbus_amqp_producer_data && poetry install
	cd nextbus_amqp_producer_amqp_producer && poetry install
	pip install ./nextbus_amqp_producer_data ./nextbus_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./nextbus_amqp_producer_amqp_producer/tests ./nextbus_amqp_producer_data/tests
