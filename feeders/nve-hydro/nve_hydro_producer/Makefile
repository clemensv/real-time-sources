.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./nve_hydro_producer_data ./nve_hydro_producer_kafka_producer

install: build
	cd nve_hydro_producer_data && poetry install
	cd nve_hydro_producer_kafka_producer && poetry install
	pip install ./nve_hydro_producer_data ./nve_hydro_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./nve_hydro_producer_kafka_producer/tests ./nve_hydro_producer_data/tests