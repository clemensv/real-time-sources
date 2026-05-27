.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./autobahn_amqp_producer_data ./autobahn_amqp_producer_amqp_producer

install: build
	cd autobahn_amqp_producer_data && poetry install
	cd autobahn_amqp_producer_amqp_producer && poetry install
	pip install ./autobahn_amqp_producer_data ./autobahn_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./autobahn_amqp_producer_amqp_producer/tests ./autobahn_amqp_producer_data/tests
