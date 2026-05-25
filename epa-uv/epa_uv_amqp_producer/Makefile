.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./epa_uv_amqp_producer_data ./epa_uv_amqp_producer_amqp_producer

install: build
	cd epa_uv_amqp_producer_data && poetry install
	cd epa_uv_amqp_producer_amqp_producer && poetry install
	pip install ./epa_uv_amqp_producer_data ./epa_uv_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./epa_uv_amqp_producer_amqp_producer/tests ./epa_uv_amqp_producer_data/tests
