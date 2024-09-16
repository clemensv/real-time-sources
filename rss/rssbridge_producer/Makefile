.PHONY: build install

build:
	pip install wheel
	pip wheel -w whl ./rssbridge_producer_data ./rssbridge_producer_kafka_producer

install: build
	pip install ./rssbridge_producer_data ./rssbridge_producer_kafka_producer

test: install
	pytest ./rssbridge_producer_kafka_producer/tests ./rssbridge_producer_data/tests