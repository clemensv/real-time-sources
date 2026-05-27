.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./aisstream_amqp_producer_data ./aisstream_amqp_producer_amqp_producer

install: build
	cd aisstream_amqp_producer_data && poetry install
	cd aisstream_amqp_producer_amqp_producer && poetry install
	pip install ./aisstream_amqp_producer_data ./aisstream_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./aisstream_amqp_producer_amqp_producer/tests ./aisstream_amqp_producer_data/tests
