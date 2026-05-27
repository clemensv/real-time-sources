.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./laqn_london_producer_data ./laqn_london_producer_kafka_producer

install: build
	cd laqn_london_producer_data && poetry install
	cd laqn_london_producer_kafka_producer && poetry install
	pip install ./laqn_london_producer_data ./laqn_london_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./laqn_london_producer_kafka_producer/tests ./laqn_london_producer_data/tests