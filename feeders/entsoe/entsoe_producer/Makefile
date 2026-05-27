.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./entsoe_producer_data ./entsoe_producer_kafka_producer

install: build
	cd entsoe_producer_data && poetry install
	cd entsoe_producer_kafka_producer && poetry install
	pip install ./entsoe_producer_data ./entsoe_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./entsoe_producer_kafka_producer/tests ./entsoe_producer_data/tests