.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./billetto_producer_data ./billetto_producer_kafka_producer

install: build
	cd billetto_producer_data && poetry install
	cd billetto_producer_kafka_producer && poetry install
	pip install ./billetto_producer_data ./billetto_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./billetto_producer_kafka_producer/tests ./billetto_producer_data/tests