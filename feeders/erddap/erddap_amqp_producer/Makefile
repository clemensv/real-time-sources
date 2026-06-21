.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./erddap_amqp_producer_data ./erddap_amqp_producer_amqp_producer

install: build
	cd erddap_amqp_producer_data && poetry install
	cd erddap_amqp_producer_amqp_producer && poetry install
	pip install ./erddap_amqp_producer_data ./erddap_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./erddap_amqp_producer_amqp_producer/tests ./erddap_amqp_producer_data/tests
