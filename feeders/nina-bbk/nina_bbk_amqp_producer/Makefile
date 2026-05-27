.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./nina_bbk_amqp_producer_data ./nina_bbk_amqp_producer_amqp_producer

install: build
	cd nina_bbk_amqp_producer_data && poetry install
	cd nina_bbk_amqp_producer_amqp_producer && poetry install
	pip install ./nina_bbk_amqp_producer_data ./nina_bbk_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./nina_bbk_amqp_producer_amqp_producer/tests ./nina_bbk_amqp_producer_data/tests
