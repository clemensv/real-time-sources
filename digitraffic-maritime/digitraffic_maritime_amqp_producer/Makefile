.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./digitraffic_maritime_amqp_producer_data ./digitraffic_maritime_amqp_producer_amqp_producer

install: build
	cd digitraffic_maritime_amqp_producer_data && poetry install
	cd digitraffic_maritime_amqp_producer_amqp_producer && poetry install
	pip install ./digitraffic_maritime_amqp_producer_data ./digitraffic_maritime_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./digitraffic_maritime_amqp_producer_amqp_producer/tests ./digitraffic_maritime_amqp_producer_data/tests
