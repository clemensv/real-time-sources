.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./bluesky_producer_data ./bluesky_producer_kafka_producer

install: build
	cd bluesky_producer_data && poetry install
	cd bluesky_producer_kafka_producer && poetry install
	pip install ./bluesky_producer_data ./bluesky_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./bluesky_producer_kafka_producer/tests ./bluesky_producer_data/tests