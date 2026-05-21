.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./tepco_denkiyoho_producer_data ./tepco_denkiyoho_producer_kafka_producer

install: build
	cd tepco_denkiyoho_producer_data && poetry install
	cd tepco_denkiyoho_producer_kafka_producer && poetry install
	pip install ./tepco_denkiyoho_producer_data ./tepco_denkiyoho_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./tepco_denkiyoho_producer_kafka_producer/tests ./tepco_denkiyoho_producer_data/tests