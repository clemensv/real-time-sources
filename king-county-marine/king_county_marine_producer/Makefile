.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./king_county_marine_producer_data ./king_county_marine_producer_kafka_producer

install: build
	cd king_county_marine_producer_data && poetry install
	cd king_county_marine_producer_kafka_producer && poetry install
	pip install ./king_county_marine_producer_data ./king_county_marine_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./king_county_marine_producer_kafka_producer/tests ./king_county_marine_producer_data/tests