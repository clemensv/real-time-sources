.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./wallonia_issep_producer_data ./wallonia_issep_producer_kafka_producer

install: build
	cd wallonia_issep_producer_data && poetry install
	cd wallonia_issep_producer_kafka_producer && poetry install
	pip install ./wallonia_issep_producer_data ./wallonia_issep_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./wallonia_issep_producer_kafka_producer/tests ./wallonia_issep_producer_data/tests