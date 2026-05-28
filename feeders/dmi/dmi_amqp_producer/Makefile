.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./dmi_amqp_producer_data ./dmi_amqp_producer_amqp_producer

install: build
	cd dmi_amqp_producer_data && poetry install
	cd dmi_amqp_producer_amqp_producer && poetry install
	pip install ./dmi_amqp_producer_data ./dmi_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./dmi_amqp_producer_amqp_producer/tests ./dmi_amqp_producer_data/tests
