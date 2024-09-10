.PHONY: build install

build:
	pip install wheel
	pip wheel -w whl ./gtfs_rt_producer_data ./gtfs_rt_producer_kafka_producer

install: build
	pip install ./gtfs_rt_producer_data ./gtfs_rt_producer_kafka_producer

test: install
	pytest ./gtfs_rt_producer_kafka_producer/tests ./gtfs_rt_producer_data/tests