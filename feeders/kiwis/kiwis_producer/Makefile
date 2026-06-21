.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./kiwis_producer_data ./kiwis_producer_kafka_producer

install: build
	cd kiwis_producer_data && poetry install
	cd kiwis_producer_kafka_producer && poetry install
	pip install ./kiwis_producer_data ./kiwis_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./kiwis_producer_kafka_producer/tests ./kiwis_producer_data/tests