.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./nepal_bipad_hydrology_producer_data ./nepal_bipad_hydrology_producer_kafka_producer

install: build
	cd nepal_bipad_hydrology_producer_data && poetry install
	cd nepal_bipad_hydrology_producer_kafka_producer && poetry install
	pip install ./nepal_bipad_hydrology_producer_data ./nepal_bipad_hydrology_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./nepal_bipad_hydrology_producer_kafka_producer/tests ./nepal_bipad_hydrology_producer_data/tests