.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./usgs_iv_producer_data ./usgs_iv_producer_kafka_producer

install: build
	cd usgs_iv_producer_data && poetry install
	cd usgs_iv_producer_kafka_producer && poetry install
	pip install ./usgs_iv_producer_data ./usgs_iv_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./usgs_iv_producer_kafka_producer/tests ./usgs_iv_producer_data/tests