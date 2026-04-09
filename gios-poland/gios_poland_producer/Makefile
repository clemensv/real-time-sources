.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./gios_poland_producer_data ./gios_poland_producer_kafka_producer

install: build
	cd gios_poland_producer_data && poetry install
	cd gios_poland_producer_kafka_producer && poetry install
	pip install ./gios_poland_producer_data ./gios_poland_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./gios_poland_producer_kafka_producer/tests ./gios_poland_producer_data/tests