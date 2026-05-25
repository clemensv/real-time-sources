.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./seattle_911_amqp_producer_data ./seattle_911_amqp_producer_amqp_producer

install: build
	cd seattle_911_amqp_producer_data && poetry install
	cd seattle_911_amqp_producer_amqp_producer && poetry install
	pip install ./seattle_911_amqp_producer_data ./seattle_911_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./seattle_911_amqp_producer_amqp_producer/tests ./seattle_911_amqp_producer_data/tests
