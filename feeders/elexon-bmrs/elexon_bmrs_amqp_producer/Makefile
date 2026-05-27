.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./elexon_bmrs_amqp_producer_data ./elexon_bmrs_amqp_producer_amqp_producer

install: build
	cd elexon_bmrs_amqp_producer_data && poetry install
	cd elexon_bmrs_amqp_producer_amqp_producer && poetry install
	pip install ./elexon_bmrs_amqp_producer_data ./elexon_bmrs_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./elexon_bmrs_amqp_producer_amqp_producer/tests ./elexon_bmrs_amqp_producer_data/tests
