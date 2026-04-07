.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./irail_producer_data ./irail_producer_kafka_producer

install: build
	cd irail_producer_data && poetry install
	cd irail_producer_kafka_producer && poetry install
	pip install ./irail_producer_data ./irail_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./irail_producer_kafka_producer/tests ./irail_producer_data/tests