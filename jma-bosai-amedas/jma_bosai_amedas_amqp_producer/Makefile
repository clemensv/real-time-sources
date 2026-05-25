.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./jma_bosai_amedas_amqp_producer_data ./jma_bosai_amedas_amqp_producer_amqp_producer

install: build
	cd jma_bosai_amedas_amqp_producer_data && poetry install
	cd jma_bosai_amedas_amqp_producer_amqp_producer && poetry install
	pip install ./jma_bosai_amedas_amqp_producer_data ./jma_bosai_amedas_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./jma_bosai_amedas_amqp_producer_amqp_producer/tests ./jma_bosai_amedas_amqp_producer_data/tests
