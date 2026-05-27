.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./rws_waterwebservices_amqp_producer_data ./rws_waterwebservices_amqp_producer_amqp_producer

install: build
	cd rws_waterwebservices_amqp_producer_data && poetry install
	cd rws_waterwebservices_amqp_producer_amqp_producer && poetry install
	pip install ./rws_waterwebservices_amqp_producer_data ./rws_waterwebservices_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./rws_waterwebservices_amqp_producer_amqp_producer/tests ./rws_waterwebservices_amqp_producer_data/tests
