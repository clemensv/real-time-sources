.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./ticketmaster_amqp_producer_data ./ticketmaster_amqp_producer_amqp_producer

install: build
	cd ticketmaster_amqp_producer_data && poetry install
	cd ticketmaster_amqp_producer_amqp_producer && poetry install
	pip install ./ticketmaster_amqp_producer_data ./ticketmaster_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./ticketmaster_amqp_producer_amqp_producer/tests ./ticketmaster_amqp_producer_data/tests
