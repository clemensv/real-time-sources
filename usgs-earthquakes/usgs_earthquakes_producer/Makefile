.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./usgs-earthquakes-producer_data ./usgs-earthquakes-producer_kafka_producer

install: build
	cd usgs-earthquakes-producer_data && poetry install
	cd usgs-earthquakes-producer_kafka_producer && poetry install
	pip install ./usgs-earthquakes-producer_data ./usgs-earthquakes-producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./usgs-earthquakes-producer_kafka_producer/tests ./usgs-earthquakes-producer_data/tests