.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./ptwc_tsunami_producer_data ./ptwc_tsunami_producer_kafka_producer

install: build
	cd ptwc_tsunami_producer_data && poetry install
	cd ptwc_tsunami_producer_kafka_producer && poetry install
	pip install ./ptwc_tsunami_producer_data ./ptwc_tsunami_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./ptwc_tsunami_producer_kafka_producer/tests ./ptwc_tsunami_producer_data/tests