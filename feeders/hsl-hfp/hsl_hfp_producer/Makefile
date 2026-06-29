.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./hsl_hfp_producer_data ./hsl_hfp_producer_kafka_producer

install: build
	cd hsl_hfp_producer_data && poetry install
	cd hsl_hfp_producer_kafka_producer && poetry install
	pip install ./hsl_hfp_producer_data ./hsl_hfp_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./hsl_hfp_producer_kafka_producer/tests ./hsl_hfp_producer_data/tests