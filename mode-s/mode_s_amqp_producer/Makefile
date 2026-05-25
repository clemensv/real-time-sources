.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./mode_s_amqp_producer_data ./mode_s_amqp_producer_amqp_producer

install: build
	cd mode_s_amqp_producer_data && poetry install
	cd mode_s_amqp_producer_amqp_producer && poetry install
	pip install ./mode_s_amqp_producer_data ./mode_s_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./mode_s_amqp_producer_amqp_producer/tests ./mode_s_amqp_producer_data/tests
