.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./seattle_911_producer_data ./seattle_911_producer_kafka_producer

install: build
	cd seattle_911_producer_data && poetry install
	cd seattle_911_producer_kafka_producer && poetry install
	pip install ./seattle_911_producer_data ./seattle_911_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./seattle_911_producer_kafka_producer/tests ./seattle_911_producer_data/tests