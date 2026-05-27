.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./snotel_producer_data ./snotel_producer_kafka_producer

install: build
	cd snotel_producer_data && poetry install
	cd snotel_producer_kafka_producer && poetry install
	pip install ./snotel_producer_data ./snotel_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./snotel_producer_kafka_producer/tests ./snotel_producer_data/tests