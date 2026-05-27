.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./usgs_earthquakes_producer_data ./usgs_earthquakes_producer_kafka_producer

install: build
	cd usgs_earthquakes_producer_data && poetry install
	cd usgs_earthquakes_producer_kafka_producer && poetry install
	pip install ./usgs_earthquakes_producer_data ./usgs_earthquakes_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./usgs_earthquakes_producer_kafka_producer/tests ./usgs_earthquakes_producer_data/tests