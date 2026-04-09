.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./epa_uv_producer_data ./epa_uv_producer_kafka_producer

install: build
	cd epa_uv_producer_data && poetry install
	cd epa_uv_producer_kafka_producer && poetry install
	pip install ./epa_uv_producer_data ./epa_uv_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./epa_uv_producer_kafka_producer/tests ./epa_uv_producer_data/tests