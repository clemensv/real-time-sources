.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./nws_forecasts_producer_data ./nws_forecasts_producer_kafka_producer

install: build
	cd nws_forecasts_producer_data && poetry install
	cd nws_forecasts_producer_kafka_producer && poetry install
	pip install ./nws_forecasts_producer_data ./nws_forecasts_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./nws_forecasts_producer_kafka_producer/tests ./nws_forecasts_producer_data/tests