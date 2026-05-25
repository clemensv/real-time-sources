.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./german_waters_amqp_producer_data ./german_waters_amqp_producer_amqp_producer

install: build
	cd german_waters_amqp_producer_data && poetry install
	cd german_waters_amqp_producer_amqp_producer && poetry install
	pip install ./german_waters_amqp_producer_data ./german_waters_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./german_waters_amqp_producer_amqp_producer/tests ./german_waters_amqp_producer_data/tests
