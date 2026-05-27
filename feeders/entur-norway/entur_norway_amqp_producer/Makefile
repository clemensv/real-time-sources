.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./entur_norway_amqp_producer_data ./entur_norway_amqp_producer_amqp_producer

install: build
	cd entur_norway_amqp_producer_data && poetry install
	cd entur_norway_amqp_producer_amqp_producer && poetry install
	pip install ./entur_norway_amqp_producer_data ./entur_norway_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./entur_norway_amqp_producer_amqp_producer/tests ./entur_norway_amqp_producer_data/tests
