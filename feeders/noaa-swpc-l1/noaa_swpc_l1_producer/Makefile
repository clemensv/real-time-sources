.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./noaa_swpc_l1_producer_data ./noaa_swpc_l1_producer_kafka_producer

install: build
	cd noaa_swpc_l1_producer_data && poetry install
	cd noaa_swpc_l1_producer_kafka_producer && poetry install
	pip install ./noaa_swpc_l1_producer_data ./noaa_swpc_l1_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./noaa_swpc_l1_producer_kafka_producer/tests ./noaa_swpc_l1_producer_data/tests