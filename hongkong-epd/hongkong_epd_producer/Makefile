.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./hongkong_epd_producer_data ./hongkong_epd_producer_kafka_producer

install: build
	cd hongkong_epd_producer_data && poetry install
	cd hongkong_epd_producer_kafka_producer && poetry install
	pip install ./hongkong_epd_producer_data ./hongkong_epd_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./hongkong_epd_producer_kafka_producer/tests ./hongkong_epd_producer_data/tests