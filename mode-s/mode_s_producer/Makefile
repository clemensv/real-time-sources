.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./mode_s_producer_data ./mode_s_producer_kafka_producer

install: build
	cd mode_s_producer_data && poetry install
	cd mode_s_producer_kafka_producer && poetry install
	pip install ./mode_s_producer_data ./mode_s_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./mode_s_producer_kafka_producer/tests ./mode_s_producer_data/tests