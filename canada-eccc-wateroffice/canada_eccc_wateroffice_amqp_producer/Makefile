.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./canada_eccc_wateroffice_amqp_producer_data ./canada_eccc_wateroffice_amqp_producer_amqp_producer

install: build
	cd canada_eccc_wateroffice_amqp_producer_data && poetry install
	cd canada_eccc_wateroffice_amqp_producer_amqp_producer && poetry install
	pip install ./canada_eccc_wateroffice_amqp_producer_data ./canada_eccc_wateroffice_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./canada_eccc_wateroffice_amqp_producer_amqp_producer/tests ./canada_eccc_wateroffice_amqp_producer_data/tests
