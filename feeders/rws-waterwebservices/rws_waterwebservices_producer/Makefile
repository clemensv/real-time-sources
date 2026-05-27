.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./rws_waterwebservices_producer_data ./rws_waterwebservices_producer_kafka_producer

install: build
	cd rws_waterwebservices_producer_data && poetry install
	cd rws_waterwebservices_producer_kafka_producer && poetry install
	pip install ./rws_waterwebservices_producer_data ./rws_waterwebservices_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./rws_waterwebservices_producer_kafka_producer/tests ./rws_waterwebservices_producer_data/tests