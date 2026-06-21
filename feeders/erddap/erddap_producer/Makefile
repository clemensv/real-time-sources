.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./erddap_producer_data ./erddap_producer_kafka_producer

install: build
	cd erddap_producer_data && poetry install
	cd erddap_producer_kafka_producer && poetry install
	pip install ./erddap_producer_data ./erddap_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./erddap_producer_kafka_producer/tests ./erddap_producer_data/tests