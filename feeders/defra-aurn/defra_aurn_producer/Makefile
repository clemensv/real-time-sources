.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./defra_aurn_producer_data ./defra_aurn_producer_kafka_producer

install: build
	cd defra_aurn_producer_data && poetry install
	cd defra_aurn_producer_kafka_producer && poetry install
	pip install ./defra_aurn_producer_data ./defra_aurn_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./defra_aurn_producer_kafka_producer/tests ./defra_aurn_producer_data/tests