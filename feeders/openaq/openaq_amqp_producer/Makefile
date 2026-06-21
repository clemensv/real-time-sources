.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./openaq_amqp_producer_data ./openaq_amqp_producer_amqp_producer

install: build
	cd openaq_amqp_producer_data && poetry install
	cd openaq_amqp_producer_amqp_producer && poetry install
	pip install ./openaq_amqp_producer_data ./openaq_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./openaq_amqp_producer_amqp_producer/tests ./openaq_amqp_producer_data/tests
