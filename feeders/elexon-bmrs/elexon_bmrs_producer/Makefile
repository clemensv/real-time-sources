.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./elexon_bmrs_producer_data ./elexon_bmrs_producer_kafka_producer

install: build
	cd elexon_bmrs_producer_data && poetry install
	cd elexon_bmrs_producer_kafka_producer && poetry install
	pip install ./elexon_bmrs_producer_data ./elexon_bmrs_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./elexon_bmrs_producer_kafka_producer/tests ./elexon_bmrs_producer_data/tests