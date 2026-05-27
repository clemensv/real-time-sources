.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./uba_airdata_producer_data ./uba_airdata_producer_kafka_producer

install: build
	cd uba_airdata_producer_data && poetry install
	cd uba_airdata_producer_kafka_producer && poetry install
	pip install ./uba_airdata_producer_data ./uba_airdata_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./uba_airdata_producer_kafka_producer/tests ./uba_airdata_producer_data/tests