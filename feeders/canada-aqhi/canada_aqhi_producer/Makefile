.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./canada_aqhi_producer_data ./canada_aqhi_producer_kafka_producer

install: build
	cd canada_aqhi_producer_data && poetry install
	cd canada_aqhi_producer_kafka_producer && poetry install
	pip install ./canada_aqhi_producer_data ./canada_aqhi_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./canada_aqhi_producer_kafka_producer/tests ./canada_aqhi_producer_data/tests