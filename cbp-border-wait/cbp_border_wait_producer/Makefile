.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./cbp_border_wait_producer_data ./cbp_border_wait_producer_kafka_producer

install: build
	cd cbp_border_wait_producer_data && poetry install
	cd cbp_border_wait_producer_kafka_producer && poetry install
	pip install ./cbp_border_wait_producer_data ./cbp_border_wait_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./cbp_border_wait_producer_kafka_producer/tests ./cbp_border_wait_producer_data/tests