.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./gdacs_producer_data ./gdacs_producer_kafka_producer

install: build
	cd gdacs_producer_data && poetry install
	cd gdacs_producer_kafka_producer && poetry install
	pip install ./gdacs_producer_data ./gdacs_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./gdacs_producer_kafka_producer/tests ./gdacs_producer_data/tests