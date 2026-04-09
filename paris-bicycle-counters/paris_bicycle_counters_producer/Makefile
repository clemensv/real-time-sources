.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./paris_bicycle_counters_producer_data ./paris_bicycle_counters_producer_kafka_producer

install: build
	cd paris_bicycle_counters_producer_data && poetry install
	cd paris_bicycle_counters_producer_kafka_producer && poetry install
	pip install ./paris_bicycle_counters_producer_data ./paris_bicycle_counters_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./paris_bicycle_counters_producer_kafka_producer/tests ./paris_bicycle_counters_producer_data/tests