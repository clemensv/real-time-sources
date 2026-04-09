.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./jma_japan_producer_data ./jma_japan_producer_kafka_producer

install: build
	cd jma_japan_producer_data && poetry install
	cd jma_japan_producer_kafka_producer && poetry install
	pip install ./jma_japan_producer_data ./jma_japan_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./jma_japan_producer_kafka_producer/tests ./jma_japan_producer_data/tests