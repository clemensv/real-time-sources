.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./nextbus_producer_data ./nextbus_producer_kafka_producer

install: build
	cd nextbus_producer_data && poetry install
	cd nextbus_producer_kafka_producer && poetry install
	pip install ./nextbus_producer_data ./nextbus_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./nextbus_producer_kafka_producer/tests ./nextbus_producer_data/tests