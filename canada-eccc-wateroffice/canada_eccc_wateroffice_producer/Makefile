.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./canada_eccc_wateroffice_producer_data ./canada_eccc_wateroffice_producer_kafka_producer

install: build
	cd canada_eccc_wateroffice_producer_data && poetry install
	cd canada_eccc_wateroffice_producer_kafka_producer && poetry install
	pip install ./canada_eccc_wateroffice_producer_data ./canada_eccc_wateroffice_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./canada_eccc_wateroffice_producer_kafka_producer/tests ./canada_eccc_wateroffice_producer_data/tests