.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./imgw_hydro_producer_data ./imgw_hydro_producer_kafka_producer

install: build
	cd imgw_hydro_producer_data && poetry install
	cd imgw_hydro_producer_kafka_producer && poetry install
	pip install ./imgw_hydro_producer_data ./imgw_hydro_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./imgw_hydro_producer_kafka_producer/tests ./imgw_hydro_producer_data/tests