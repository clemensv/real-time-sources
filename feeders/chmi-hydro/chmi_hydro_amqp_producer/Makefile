.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./chmi_hydro_amqp_producer_data ./chmi_hydro_amqp_producer_amqp_producer

install: build
	cd chmi_hydro_amqp_producer_data && poetry install
	cd chmi_hydro_amqp_producer_amqp_producer && poetry install
	pip install ./chmi_hydro_amqp_producer_data ./chmi_hydro_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./chmi_hydro_amqp_producer_amqp_producer/tests ./chmi_hydro_amqp_producer_data/tests
