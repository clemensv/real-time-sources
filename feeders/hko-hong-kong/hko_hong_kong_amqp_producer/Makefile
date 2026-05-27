.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./hko_hong_kong_amqp_producer_data ./hko_hong_kong_amqp_producer_amqp_producer

install: build
	cd hko_hong_kong_amqp_producer_data && poetry install
	cd hko_hong_kong_amqp_producer_amqp_producer && poetry install
	pip install ./hko_hong_kong_amqp_producer_data ./hko_hong_kong_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./hko_hong_kong_amqp_producer_amqp_producer/tests ./hko_hong_kong_amqp_producer_data/tests
