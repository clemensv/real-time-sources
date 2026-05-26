.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./fienta_amqp_producer_data ./fienta_amqp_producer_amqp_producer

install: build
	cd fienta_amqp_producer_data && poetry install
	cd fienta_amqp_producer_amqp_producer && poetry install
	pip install ./fienta_amqp_producer_data ./fienta_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./fienta_amqp_producer_amqp_producer/tests ./fienta_amqp_producer_data/tests
