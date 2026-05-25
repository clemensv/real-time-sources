.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./xceed_amqp_producer_data ./xceed_amqp_producer_amqp_producer

install: build
	cd xceed_amqp_producer_data && poetry install
	cd xceed_amqp_producer_amqp_producer && poetry install
	pip install ./xceed_amqp_producer_data ./xceed_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./xceed_amqp_producer_amqp_producer/tests ./xceed_amqp_producer_data/tests
