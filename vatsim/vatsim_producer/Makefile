.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./vatsim_producer_data ./vatsim_producer_kafka_producer

install: build
	cd vatsim_producer_data && poetry install
	cd vatsim_producer_kafka_producer && poetry install
	pip install ./vatsim_producer_data ./vatsim_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./vatsim_producer_kafka_producer/tests ./vatsim_producer_data/tests