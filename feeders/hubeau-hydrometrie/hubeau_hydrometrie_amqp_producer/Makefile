.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./hubeau_hydrometrie_amqp_producer_data ./hubeau_hydrometrie_amqp_producer_amqp_producer

install: build
	cd hubeau_hydrometrie_amqp_producer_data && poetry install
	cd hubeau_hydrometrie_amqp_producer_amqp_producer && poetry install
	pip install ./hubeau_hydrometrie_amqp_producer_data ./hubeau_hydrometrie_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./hubeau_hydrometrie_amqp_producer_amqp_producer/tests ./hubeau_hydrometrie_amqp_producer_data/tests
