.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./rssbridge_producer_data ./rssbridge_producer_kafka_producer

install: build
	cd rssbridge_producer_data && poetry install
	cd rssbridge_producer_kafka_producer && poetry install
	pip install ./rssbridge_producer_data ./rssbridge_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./rssbridge_producer_kafka_producer/tests ./rssbridge_producer_data/tests