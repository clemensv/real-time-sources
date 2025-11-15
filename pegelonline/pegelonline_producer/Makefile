.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./pegelonline_producer_data ./pegelonline_producer_kafka_producer

install: build
	cd pegelonline_producer_data && poetry install
	cd pegelonline_producer_kafka_producer && poetry install
	pip install ./pegelonline_producer_data ./pegelonline_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./pegelonline_producer_kafka_producer/tests ./pegelonline_producer_data/tests