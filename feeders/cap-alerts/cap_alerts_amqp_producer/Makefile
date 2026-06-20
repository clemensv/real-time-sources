.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./cap_alerts_amqp_producer_data ./cap_alerts_amqp_producer_amqp_producer

install: build
	cd cap_alerts_amqp_producer_data && poetry install
	cd cap_alerts_amqp_producer_amqp_producer && poetry install
	pip install ./cap_alerts_amqp_producer_data ./cap_alerts_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./cap_alerts_amqp_producer_amqp_producer/tests ./cap_alerts_amqp_producer_data/tests
