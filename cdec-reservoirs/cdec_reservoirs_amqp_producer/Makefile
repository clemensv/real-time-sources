.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./cdec_reservoirs_amqp_producer_data ./cdec_reservoirs_amqp_producer_amqp_producer

install: build
	cd cdec_reservoirs_amqp_producer_data && poetry install
	cd cdec_reservoirs_amqp_producer_amqp_producer && poetry install
	pip install ./cdec_reservoirs_amqp_producer_data ./cdec_reservoirs_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./cdec_reservoirs_amqp_producer_amqp_producer/tests ./cdec_reservoirs_amqp_producer_data/tests
