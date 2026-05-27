.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./gracedb_producer_data ./gracedb_producer_kafka_producer

install: build
	cd gracedb_producer_data && poetry install
	cd gracedb_producer_kafka_producer && poetry install
	pip install ./gracedb_producer_data ./gracedb_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./gracedb_producer_kafka_producer/tests ./gracedb_producer_data/tests