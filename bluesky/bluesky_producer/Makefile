.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./bluesky-producer_data ./bluesky-producer_kafka_producer

install: build
	cd bluesky-producer_data && poetry install
	cd bluesky-producer_kafka_producer && poetry install
	pip install ./bluesky-producer_data ./bluesky-producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./bluesky-producer_kafka_producer/tests ./bluesky-producer_data/tests