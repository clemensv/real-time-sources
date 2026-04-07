.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./wikimedia_eventstreams_producer_data ./wikimedia_eventstreams_producer_kafka_producer

install: build
	cd wikimedia_eventstreams_producer_data && poetry install
	cd wikimedia_eventstreams_producer_kafka_producer && poetry install
	pip install ./wikimedia_eventstreams_producer_data ./wikimedia_eventstreams_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./wikimedia_eventstreams_producer_kafka_producer/tests ./wikimedia_eventstreams_producer_data/tests