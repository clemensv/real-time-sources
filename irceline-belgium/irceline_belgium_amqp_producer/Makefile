.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./irceline_belgium_amqp_producer_data ./irceline_belgium_amqp_producer_amqp_producer

install: build
	cd irceline_belgium_amqp_producer_data && poetry install
	cd irceline_belgium_amqp_producer_amqp_producer && poetry install
	pip install ./irceline_belgium_amqp_producer_data ./irceline_belgium_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./irceline_belgium_amqp_producer_amqp_producer/tests ./irceline_belgium_amqp_producer_data/tests
