.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./kystverket_ais_producer_data ./kystverket_ais_producer_kafka_producer

install: build
	cd kystverket_ais_producer_data && poetry install
	cd kystverket_ais_producer_kafka_producer && poetry install
	pip install ./kystverket_ais_producer_data ./kystverket_ais_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./kystverket_ais_producer_kafka_producer/tests ./kystverket_ais_producer_data/tests