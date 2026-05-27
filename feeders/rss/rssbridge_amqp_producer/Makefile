.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./rssbridge_amqp_producer_data ./rssbridge_amqp_producer_amqp_producer

install: build
	cd rssbridge_amqp_producer_data && poetry install
	cd rssbridge_amqp_producer_amqp_producer && poetry install
	pip install ./rssbridge_amqp_producer_data ./rssbridge_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./rssbridge_amqp_producer_amqp_producer/tests ./rssbridge_amqp_producer_data/tests
