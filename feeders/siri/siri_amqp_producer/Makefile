.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./siri_amqp_producer_data ./siri_amqp_producer_amqp_producer

install: build
	cd siri_amqp_producer_data && poetry install
	cd siri_amqp_producer_amqp_producer && poetry install
	pip install ./siri_amqp_producer_data ./siri_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./siri_amqp_producer_amqp_producer/tests ./siri_amqp_producer_data/tests
