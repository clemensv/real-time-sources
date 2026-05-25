.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./wallonia_issep_amqp_producer_data ./wallonia_issep_amqp_producer_amqp_producer

install: build
	cd wallonia_issep_amqp_producer_data && poetry install
	cd wallonia_issep_amqp_producer_amqp_producer && poetry install
	pip install ./wallonia_issep_amqp_producer_data ./wallonia_issep_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./wallonia_issep_amqp_producer_amqp_producer/tests ./wallonia_issep_amqp_producer_data/tests
