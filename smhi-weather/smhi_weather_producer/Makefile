.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./smhi_weather_producer_data ./smhi_weather_producer_kafka_producer

install: build
	cd smhi_weather_producer_data && poetry install
	cd smhi_weather_producer_kafka_producer && poetry install
	pip install ./smhi_weather_producer_data ./smhi_weather_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./smhi_weather_producer_kafka_producer/tests ./smhi_weather_producer_data/tests