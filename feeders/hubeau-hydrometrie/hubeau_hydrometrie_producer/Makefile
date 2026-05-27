.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./hubeau_hydrometrie_producer_data ./hubeau_hydrometrie_producer_kafka_producer

install: build
	cd hubeau_hydrometrie_producer_data && poetry install
	cd hubeau_hydrometrie_producer_kafka_producer && poetry install
	pip install ./hubeau_hydrometrie_producer_data ./hubeau_hydrometrie_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./hubeau_hydrometrie_producer_kafka_producer/tests ./hubeau_hydrometrie_producer_data/tests