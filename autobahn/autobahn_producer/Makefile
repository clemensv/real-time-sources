.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./autobahn_producer_data ./autobahn_producer_kafka_producer

install: build
	cd autobahn_producer_data && poetry install
	cd autobahn_producer_kafka_producer && poetry install
	pip install ./autobahn_producer_data ./autobahn_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./autobahn_producer_kafka_producer/tests ./autobahn_producer_data/tests