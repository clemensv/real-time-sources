.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./nve_hydro_amqp_producer_data ./nve_hydro_amqp_producer_amqp_producer

install: build
	cd nve_hydro_amqp_producer_data && poetry install
	cd nve_hydro_amqp_producer_amqp_producer && poetry install
	pip install ./nve_hydro_amqp_producer_data ./nve_hydro_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./nve_hydro_amqp_producer_amqp_producer/tests ./nve_hydro_amqp_producer_data/tests
