.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./taipei_youbike_producer_data ./taipei_youbike_producer_kafka_producer

install: build
	cd taipei_youbike_producer_data && poetry install
	cd taipei_youbike_producer_kafka_producer && poetry install
	pip install ./taipei_youbike_producer_data ./taipei_youbike_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./taipei_youbike_producer_kafka_producer/tests ./taipei_youbike_producer_data/tests