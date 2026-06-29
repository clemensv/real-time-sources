.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./hsl_hfp_amqp_producer_data ./hsl_hfp_amqp_producer_amqp_producer

install: build
	cd hsl_hfp_amqp_producer_data && poetry install
	cd hsl_hfp_amqp_producer_amqp_producer && poetry install
	pip install ./hsl_hfp_amqp_producer_data ./hsl_hfp_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./hsl_hfp_amqp_producer_amqp_producer/tests ./hsl_hfp_amqp_producer_data/tests
