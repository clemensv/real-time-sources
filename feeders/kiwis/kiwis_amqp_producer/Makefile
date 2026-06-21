.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./kiwis_amqp_producer_data ./kiwis_amqp_producer_amqp_producer

install: build
	cd kiwis_amqp_producer_data && poetry install
	cd kiwis_amqp_producer_amqp_producer && poetry install
	pip install ./kiwis_amqp_producer_data ./kiwis_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./kiwis_amqp_producer_amqp_producer/tests ./kiwis_amqp_producer_data/tests
