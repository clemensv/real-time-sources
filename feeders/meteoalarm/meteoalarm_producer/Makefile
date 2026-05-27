.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./meteoalarm_producer_data ./meteoalarm_producer_kafka_producer

install: build
	cd meteoalarm_producer_data && poetry install
	cd meteoalarm_producer_kafka_producer && poetry install
	pip install ./meteoalarm_producer_data ./meteoalarm_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./meteoalarm_producer_kafka_producer/tests ./meteoalarm_producer_data/tests