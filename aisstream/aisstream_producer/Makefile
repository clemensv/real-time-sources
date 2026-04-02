.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./aisstream_producer_data ./aisstream_producer_kafka_producer

install: build
	cd aisstream_producer_data && poetry install
	cd aisstream_producer_kafka_producer && poetry install
	pip install ./aisstream_producer_data ./aisstream_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./aisstream_producer_kafka_producer/tests ./aisstream_producer_data/tests