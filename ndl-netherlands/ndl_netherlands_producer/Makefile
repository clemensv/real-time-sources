.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./ndl_netherlands_producer_data ./ndl_netherlands_producer_kafka_producer

install: build
	cd ndl_netherlands_producer_data && poetry install
	cd ndl_netherlands_producer_kafka_producer && poetry install
	pip install ./ndl_netherlands_producer_data ./ndl_netherlands_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./ndl_netherlands_producer_kafka_producer/tests ./ndl_netherlands_producer_data/tests