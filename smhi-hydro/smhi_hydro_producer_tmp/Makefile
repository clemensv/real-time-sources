.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./smhi_hydro_producer_data ./smhi_hydro_producer_kafka_producer

install: build
	cd smhi_hydro_producer_data && poetry install
	cd smhi_hydro_producer_kafka_producer && poetry install
	pip install ./smhi_hydro_producer_data ./smhi_hydro_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./smhi_hydro_producer_kafka_producer/tests ./smhi_hydro_producer_data/tests