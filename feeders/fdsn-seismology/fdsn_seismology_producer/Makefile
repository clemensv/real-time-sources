.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./fdsn_seismology_producer_data ./fdsn_seismology_producer_kafka_producer

install: build
	cd fdsn_seismology_producer_data && poetry install
	cd fdsn_seismology_producer_kafka_producer && poetry install
	pip install ./fdsn_seismology_producer_data ./fdsn_seismology_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./fdsn_seismology_producer_kafka_producer/tests ./fdsn_seismology_producer_data/tests