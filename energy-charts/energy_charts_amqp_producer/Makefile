.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./energy_charts_amqp_producer_data ./energy_charts_amqp_producer_amqp_producer

install: build
	cd energy_charts_amqp_producer_data && poetry install
	cd energy_charts_amqp_producer_amqp_producer && poetry install
	pip install ./energy_charts_amqp_producer_data ./energy_charts_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./energy_charts_amqp_producer_amqp_producer/tests ./energy_charts_amqp_producer_data/tests
