.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./bom_australia_amqp_producer_data ./bom_australia_amqp_producer_amqp_producer

install: build
	cd bom_australia_amqp_producer_data && poetry install
	cd bom_australia_amqp_producer_amqp_producer && poetry install
	pip install ./bom_australia_amqp_producer_data ./bom_australia_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./bom_australia_amqp_producer_amqp_producer/tests ./bom_australia_amqp_producer_data/tests
