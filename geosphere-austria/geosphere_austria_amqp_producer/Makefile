.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./geosphere_austria_amqp_producer_data ./geosphere_austria_amqp_producer_amqp_producer

install: build
	cd geosphere_austria_amqp_producer_data && poetry install
	cd geosphere_austria_amqp_producer_amqp_producer && poetry install
	pip install ./geosphere_austria_amqp_producer_data ./geosphere_austria_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./geosphere_austria_amqp_producer_amqp_producer/tests ./geosphere_austria_amqp_producer_data/tests
