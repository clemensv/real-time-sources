.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./luchtmeetnet_nl_amqp_producer_data ./luchtmeetnet_nl_amqp_producer_amqp_producer

install: build
	cd luchtmeetnet_nl_amqp_producer_data && poetry install
	cd luchtmeetnet_nl_amqp_producer_amqp_producer && poetry install
	pip install ./luchtmeetnet_nl_amqp_producer_data ./luchtmeetnet_nl_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./luchtmeetnet_nl_amqp_producer_amqp_producer/tests ./luchtmeetnet_nl_amqp_producer_data/tests
