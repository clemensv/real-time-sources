.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./bafu_hydro_amqp_producer_data ./bafu_hydro_amqp_producer_amqp_producer

install: build
	cd bafu_hydro_amqp_producer_data && poetry install
	cd bafu_hydro_amqp_producer_amqp_producer && poetry install
	pip install ./bafu_hydro_amqp_producer_data ./bafu_hydro_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./bafu_hydro_amqp_producer_amqp_producer/tests ./bafu_hydro_amqp_producer_data/tests
