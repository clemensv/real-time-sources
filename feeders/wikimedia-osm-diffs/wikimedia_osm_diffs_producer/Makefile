.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./wikimedia_osm_diffs_producer_data ./wikimedia_osm_diffs_producer_kafka_producer

install: build
	cd wikimedia_osm_diffs_producer_data && poetry install
	cd wikimedia_osm_diffs_producer_kafka_producer && poetry install
	pip install ./wikimedia_osm_diffs_producer_data ./wikimedia_osm_diffs_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./wikimedia_osm_diffs_producer_kafka_producer/tests ./wikimedia_osm_diffs_producer_data/tests