.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./cdec_reservoirs_producer_data ./cdec_reservoirs_producer_kafka_producer

install: build
	cd cdec_reservoirs_producer_data && poetry install
	cd cdec_reservoirs_producer_kafka_producer && poetry install
	pip install ./cdec_reservoirs_producer_data ./cdec_reservoirs_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./cdec_reservoirs_producer_kafka_producer/tests ./cdec_reservoirs_producer_data/tests