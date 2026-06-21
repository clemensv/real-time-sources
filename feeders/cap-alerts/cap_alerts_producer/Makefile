.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./cap_alerts_producer_data ./cap_alerts_producer_kafka_producer

install: build
	cd cap_alerts_producer_data && poetry install
	cd cap_alerts_producer_kafka_producer && poetry install
	pip install ./cap_alerts_producer_data ./cap_alerts_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./cap_alerts_producer_kafka_producer/tests ./cap_alerts_producer_data/tests