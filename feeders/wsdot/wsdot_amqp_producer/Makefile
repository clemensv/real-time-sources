.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./wsdot_amqp_producer_data ./wsdot_amqp_producer_amqp_producer

install: build
	cd wsdot_amqp_producer_data && poetry install
	cd wsdot_amqp_producer_amqp_producer && poetry install
	pip install ./wsdot_amqp_producer_data ./wsdot_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./wsdot_amqp_producer_amqp_producer/tests ./wsdot_amqp_producer_data/tests
