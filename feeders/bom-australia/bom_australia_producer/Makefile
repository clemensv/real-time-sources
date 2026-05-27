.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./bom_australia_producer_data ./bom_australia_producer_kafka_producer

install: build
	cd bom_australia_producer_data && poetry install
	cd bom_australia_producer_kafka_producer && poetry install
	pip install ./bom_australia_producer_data ./bom_australia_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./bom_australia_producer_kafka_producer/tests ./bom_australia_producer_data/tests