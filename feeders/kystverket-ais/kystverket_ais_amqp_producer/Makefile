.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./kystverket_ais_amqp_producer_data ./kystverket_ais_amqp_producer_amqp_producer

install: build
	cd kystverket_ais_amqp_producer_data && poetry install
	cd kystverket_ais_amqp_producer_amqp_producer && poetry install
	pip install ./kystverket_ais_amqp_producer_data ./kystverket_ais_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./kystverket_ais_amqp_producer_amqp_producer/tests ./kystverket_ais_amqp_producer_data/tests
