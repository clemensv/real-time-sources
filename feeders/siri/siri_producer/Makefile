.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./siri_producer_data ./siri_producer_kafka_producer

install: build
	cd siri_producer_data && poetry install
	cd siri_producer_kafka_producer && poetry install
	pip install ./siri_producer_data ./siri_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./siri_producer_kafka_producer/tests ./siri_producer_data/tests