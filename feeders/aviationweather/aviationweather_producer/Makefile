.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./aviationweather_producer_data ./aviationweather_producer_kafka_producer

install: build
	cd aviationweather_producer_data && poetry install
	cd aviationweather_producer_kafka_producer && poetry install
	pip install ./aviationweather_producer_data ./aviationweather_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./aviationweather_producer_kafka_producer/tests ./aviationweather_producer_data/tests