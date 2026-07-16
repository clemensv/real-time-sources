.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./celestrak_producer_data ./celestrak_producer_kafka_producer

install: build
	cd celestrak_producer_data && poetry install
	cd celestrak_producer_kafka_producer && poetry install
	pip install ./celestrak_producer_data ./celestrak_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./celestrak_producer_kafka_producer/tests ./celestrak_producer_data/tests