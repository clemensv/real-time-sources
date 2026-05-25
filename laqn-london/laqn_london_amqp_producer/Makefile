.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./laqn_london_amqp_producer_data ./laqn_london_amqp_producer_amqp_producer

install: build
	cd laqn_london_amqp_producer_data && poetry install
	cd laqn_london_amqp_producer_amqp_producer && poetry install
	pip install ./laqn_london_amqp_producer_data ./laqn_london_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./laqn_london_amqp_producer_amqp_producer/tests ./laqn_london_amqp_producer_data/tests
