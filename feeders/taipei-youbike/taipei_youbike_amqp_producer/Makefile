.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./taipei_youbike_amqp_producer_data ./taipei_youbike_amqp_producer_amqp_producer

install: build
	cd taipei_youbike_amqp_producer_data && poetry install
	cd taipei_youbike_amqp_producer_amqp_producer && poetry install
	pip install ./taipei_youbike_amqp_producer_data ./taipei_youbike_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./taipei_youbike_amqp_producer_amqp_producer/tests ./taipei_youbike_amqp_producer_data/tests
