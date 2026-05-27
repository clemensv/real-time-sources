.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./luchtmeetnet_nl_producer_data ./luchtmeetnet_nl_producer_kafka_producer

install: build
	cd luchtmeetnet_nl_producer_data && poetry install
	cd luchtmeetnet_nl_producer_kafka_producer && poetry install
	pip install ./luchtmeetnet_nl_producer_data ./luchtmeetnet_nl_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./luchtmeetnet_nl_producer_kafka_producer/tests ./luchtmeetnet_nl_producer_data/tests