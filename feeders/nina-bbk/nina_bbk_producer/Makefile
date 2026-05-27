.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./nina_bbk_producer_data ./nina_bbk_producer_kafka_producer

install: build
	cd nina_bbk_producer_data && poetry install
	cd nina_bbk_producer_kafka_producer && poetry install
	pip install ./nina_bbk_producer_data ./nina_bbk_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./nina_bbk_producer_kafka_producer/tests ./nina_bbk_producer_data/tests