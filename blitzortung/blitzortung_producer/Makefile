.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./blitzortung_producer_data ./blitzortung_producer_kafka_producer

install: build
	cd blitzortung_producer_data && poetry install
	cd blitzortung_producer_kafka_producer && poetry install
	pip install ./blitzortung_producer_data ./blitzortung_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./blitzortung_producer_kafka_producer/tests ./blitzortung_producer_data/tests