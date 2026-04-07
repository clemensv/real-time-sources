.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./singapore_nea_producer_data ./singapore_nea_producer_kafka_producer

install: build
	cd singapore_nea_producer_data && poetry install
	cd singapore_nea_producer_kafka_producer && poetry install
	pip install ./singapore_nea_producer_data ./singapore_nea_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./singapore_nea_producer_kafka_producer/tests ./singapore_nea_producer_data/tests