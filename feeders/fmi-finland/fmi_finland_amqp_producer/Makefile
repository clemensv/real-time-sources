.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./fmi_finland_amqp_producer_data ./fmi_finland_amqp_producer_amqp_producer

install: build
	cd fmi_finland_amqp_producer_data && poetry install
	cd fmi_finland_amqp_producer_amqp_producer && poetry install
	pip install ./fmi_finland_amqp_producer_data ./fmi_finland_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./fmi_finland_amqp_producer_amqp_producer/tests ./fmi_finland_amqp_producer_data/tests
