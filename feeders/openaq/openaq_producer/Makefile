.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./openaq_producer_data ./openaq_producer_kafka_producer

install: build
	cd openaq_producer_data && poetry install
	cd openaq_producer_kafka_producer && poetry install
	pip install ./openaq_producer_data ./openaq_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./openaq_producer_kafka_producer/tests ./openaq_producer_data/tests