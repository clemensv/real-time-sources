.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./wikimedia_eventstreams_amqp_producer_data ./wikimedia_eventstreams_amqp_producer_amqp_producer

install: build
	cd wikimedia_eventstreams_amqp_producer_data && poetry install
	cd wikimedia_eventstreams_amqp_producer_amqp_producer && poetry install
	pip install ./wikimedia_eventstreams_amqp_producer_data ./wikimedia_eventstreams_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./wikimedia_eventstreams_amqp_producer_amqp_producer/tests ./wikimedia_eventstreams_amqp_producer_data/tests
