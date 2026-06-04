.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./uk_bods_siri_producer_data ./uk_bods_siri_producer_kafka_producer

install: build
	cd uk_bods_siri_producer_data && poetry install
	cd uk_bods_siri_producer_kafka_producer && poetry install
	pip install ./uk_bods_siri_producer_data ./uk_bods_siri_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./uk_bods_siri_producer_kafka_producer/tests ./uk_bods_siri_producer_data/tests