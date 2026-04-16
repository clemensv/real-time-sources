.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./xceed_producer_data ./xceed_producer_kafka_producer

install: build
	cd xceed_producer_data && poetry install
	cd xceed_producer_kafka_producer && poetry install
	pip install ./xceed_producer_data ./xceed_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./xceed_producer_kafka_producer/tests ./xceed_producer_data/tests