.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./usgs-iv-producer_data ./usgs-iv-producer_kafka_producer

install: build
	cd usgs-iv-producer_data && poetry install
	cd usgs-iv-producer_kafka_producer && poetry install
	pip install ./usgs-iv-producer_data ./usgs-iv-producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./usgs-iv-producer_kafka_producer/tests ./usgs-iv-producer_data/tests