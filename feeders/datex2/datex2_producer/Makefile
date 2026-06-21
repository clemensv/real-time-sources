.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./datex2_producer_data ./datex2_producer_kafka_producer

install: build
	cd datex2_producer_data && poetry install
	cd datex2_producer_kafka_producer && poetry install
	pip install ./datex2_producer_data ./datex2_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./datex2_producer_kafka_producer/tests ./datex2_producer_data/tests