.PHONY: build install

build:
	pip install wheel
	pip wheel -w whl ./usgs_iv_producer_data ./usgs_iv_producer_kafka_producer

install: build
	pip install ./usgs_iv_producer_data ./usgs_iv_producer_kafka_producer

test: install
	pytest ./usgs_iv_producer_kafka_producer/tests ./usgs_iv_producer_data/tests