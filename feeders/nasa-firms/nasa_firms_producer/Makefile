.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./nasa_firms_producer_data ./nasa_firms_producer_kafka_producer

install: build
	cd nasa_firms_producer_data && poetry install
	cd nasa_firms_producer_kafka_producer && poetry install
	pip install ./nasa_firms_producer_data ./nasa_firms_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./nasa_firms_producer_kafka_producer/tests ./nasa_firms_producer_data/tests