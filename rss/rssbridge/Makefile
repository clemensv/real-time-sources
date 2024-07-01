.PHONY: build install

build:
	@python scripts/build.py

install:
	poetry install --no-root --with dev -C ./rssbridge_producer_kafka_producer
	pip install ./rssbridge_producer_kafka_producer

test: install
	pytest ./rssbridge_producer_kafka_producer/tests ./rssbridge_producer_data/tests