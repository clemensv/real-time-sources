.PHONY: build install

build:
	pip install wheel
	pip wheel -w whl ./pegelonline_producer_data ./pegelonline_producer_kafka_producer

install: build
	pip install ./pegelonline_producer_data ./pegelonline_producer_kafka_producer

test: install
	pytest ./pegelonline_producer_kafka_producer/tests ./pegelonline_producer_data/tests