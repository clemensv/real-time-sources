.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./open_charge_map_amqp_producer_data ./open_charge_map_amqp_producer_amqp_producer

install: build
	cd open_charge_map_amqp_producer_data && poetry install
	cd open_charge_map_amqp_producer_amqp_producer && poetry install
	pip install ./open_charge_map_amqp_producer_data ./open_charge_map_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./open_charge_map_amqp_producer_amqp_producer/tests ./open_charge_map_amqp_producer_data/tests
