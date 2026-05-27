.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./dwd_pollenflug_producer_data ./dwd_pollenflug_producer_kafka_producer

install: build
	cd dwd_pollenflug_producer_data && poetry install
	cd dwd_pollenflug_producer_kafka_producer && poetry install
	pip install ./dwd_pollenflug_producer_data ./dwd_pollenflug_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./dwd_pollenflug_producer_kafka_producer/tests ./dwd_pollenflug_producer_data/tests