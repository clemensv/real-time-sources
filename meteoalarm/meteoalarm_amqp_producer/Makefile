.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./meteoalarm_amqp_producer_data ./meteoalarm_amqp_producer_amqp_producer

install: build
	cd meteoalarm_amqp_producer_data && poetry install
	cd meteoalarm_amqp_producer_amqp_producer && poetry install
	pip install ./meteoalarm_amqp_producer_data ./meteoalarm_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./meteoalarm_amqp_producer_amqp_producer/tests ./meteoalarm_amqp_producer_data/tests
