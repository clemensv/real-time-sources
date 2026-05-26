.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./imgw_hydro_amqp_producer_data ./imgw_hydro_amqp_producer_amqp_producer

install: build
	cd imgw_hydro_amqp_producer_data && poetry install
	cd imgw_hydro_amqp_producer_amqp_producer && poetry install
	pip install ./imgw_hydro_amqp_producer_data ./imgw_hydro_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./imgw_hydro_amqp_producer_amqp_producer/tests ./imgw_hydro_amqp_producer_data/tests
