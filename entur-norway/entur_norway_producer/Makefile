.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./entur_norway_producer_data ./entur_norway_producer_kafka_producer

install: build
	cd entur_norway_producer_data && poetry install
	cd entur_norway_producer_kafka_producer && poetry install
	pip install ./entur_norway_producer_data ./entur_norway_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./entur_norway_producer_kafka_producer/tests ./entur_norway_producer_data/tests