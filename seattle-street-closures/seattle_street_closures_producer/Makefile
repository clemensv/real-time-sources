.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./seattle_street_closures_producer_data ./seattle_street_closures_producer_kafka_producer

install: build
	cd seattle_street_closures_producer_data && poetry install
	cd seattle_street_closures_producer_kafka_producer && poetry install
	pip install ./seattle_street_closures_producer_data ./seattle_street_closures_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./seattle_street_closures_producer_kafka_producer/tests ./seattle_street_closures_producer_data/tests