.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./ticketmaster_producer_data ./ticketmaster_producer_kafka_producer

install: build
	cd ticketmaster_producer_data && poetry install
	cd ticketmaster_producer_kafka_producer && poetry install
	pip install ./ticketmaster_producer_data ./ticketmaster_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./ticketmaster_producer_kafka_producer/tests ./ticketmaster_producer_data/tests