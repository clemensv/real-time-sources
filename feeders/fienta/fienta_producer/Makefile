.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./fienta_producer_data ./fienta_producer_kafka_producer

install: build
	cd fienta_producer_data && poetry install
	cd fienta_producer_kafka_producer && poetry install
	pip install ./fienta_producer_data ./fienta_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./fienta_producer_kafka_producer/tests ./fienta_producer_data/tests