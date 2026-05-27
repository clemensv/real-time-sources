.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./aviationweather_amqp_producer_data ./aviationweather_amqp_producer_amqp_producer

install: build
	cd aviationweather_amqp_producer_data && poetry install
	cd aviationweather_amqp_producer_amqp_producer && poetry install
	pip install ./aviationweather_amqp_producer_data ./aviationweather_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./aviationweather_amqp_producer_amqp_producer/tests ./aviationweather_amqp_producer_data/tests
