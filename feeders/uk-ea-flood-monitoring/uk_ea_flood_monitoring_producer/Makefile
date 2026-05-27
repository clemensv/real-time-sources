.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./uk_ea_flood_monitoring_producer_data ./uk_ea_flood_monitoring_producer_kafka_producer

install: build
	cd uk_ea_flood_monitoring_producer_data && poetry install
	cd uk_ea_flood_monitoring_producer_kafka_producer && poetry install
	pip install ./uk_ea_flood_monitoring_producer_data ./uk_ea_flood_monitoring_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./uk_ea_flood_monitoring_producer_kafka_producer/tests ./uk_ea_flood_monitoring_producer_data/tests