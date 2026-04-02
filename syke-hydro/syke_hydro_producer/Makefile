.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./syke_hydro_producer_data ./syke_hydro_producer_kafka_producer

install: build
	cd syke_hydro_producer_data && poetry install
	cd syke_hydro_producer_kafka_producer && poetry install
	pip install ./syke_hydro_producer_data ./syke_hydro_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./syke_hydro_producer_kafka_producer/tests ./syke_hydro_producer_data/tests