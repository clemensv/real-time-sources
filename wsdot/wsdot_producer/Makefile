.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./wsdot_producer_data ./wsdot_producer_kafka_producer

install: build
	cd wsdot_producer_data && poetry install
	cd wsdot_producer_kafka_producer && poetry install
	pip install ./wsdot_producer_data ./wsdot_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./wsdot_producer_kafka_producer/tests ./wsdot_producer_data/tests