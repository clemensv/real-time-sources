.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./uk_bods_siri_amqp_producer_data ./uk_bods_siri_amqp_producer_amqp_producer

install: build
	cd uk_bods_siri_amqp_producer_data && poetry install
	cd uk_bods_siri_amqp_producer_amqp_producer && poetry install
	pip install ./uk_bods_siri_amqp_producer_data ./uk_bods_siri_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./uk_bods_siri_amqp_producer_amqp_producer/tests ./uk_bods_siri_amqp_producer_data/tests
