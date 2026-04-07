.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./chmi_hydro_producer_data ./chmi_hydro_producer_kafka_producer

install: build
	cd chmi_hydro_producer_data && poetry install
	cd chmi_hydro_producer_kafka_producer && poetry install
	pip install ./chmi_hydro_producer_data ./chmi_hydro_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./chmi_hydro_producer_kafka_producer/tests ./chmi_hydro_producer_data/tests