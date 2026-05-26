.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./seattle_street_closures_amqp_producer_data ./seattle_street_closures_amqp_producer_amqp_producer

install: build
	cd seattle_street_closures_amqp_producer_data && poetry install
	cd seattle_street_closures_amqp_producer_amqp_producer && poetry install
	pip install ./seattle_street_closures_amqp_producer_data ./seattle_street_closures_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./seattle_street_closures_amqp_producer_amqp_producer/tests ./seattle_street_closures_amqp_producer_data/tests
