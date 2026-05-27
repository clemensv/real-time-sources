.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./vatsim_amqp_producer_data ./vatsim_amqp_producer_amqp_producer

install: build
	cd vatsim_amqp_producer_data && poetry install
	cd vatsim_amqp_producer_amqp_producer && poetry install
	pip install ./vatsim_amqp_producer_data ./vatsim_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./vatsim_amqp_producer_amqp_producer/tests ./vatsim_amqp_producer_data/tests
