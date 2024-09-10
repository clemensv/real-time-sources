.PHONY: build install

build:
	pip install setuptools wheel
	pip wheel -w whl ./gtfs_rt_producer/gtfs_rt_producer_data ./gtfs_rt_producer/gtfs_rt_producer_kafka_producer ./gtfs_rt_bridge/ 

install: build
	pip install --no-index --find-links=whl gtfs_rt_bridge
