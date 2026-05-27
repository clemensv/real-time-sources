.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./energidataservice_dk_amqp_producer_data ./energidataservice_dk_amqp_producer_amqp_producer

install: build
	cd energidataservice_dk_amqp_producer_data && poetry install
	cd energidataservice_dk_amqp_producer_amqp_producer && poetry install
	pip install ./energidataservice_dk_amqp_producer_data ./energidataservice_dk_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./energidataservice_dk_amqp_producer_amqp_producer/tests ./energidataservice_dk_amqp_producer_data/tests
