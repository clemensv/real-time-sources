.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./inpe_deter_brazil_producer_data ./inpe_deter_brazil_producer_kafka_producer

install: build
	cd inpe_deter_brazil_producer_data && poetry install
	cd inpe_deter_brazil_producer_kafka_producer && poetry install
	pip install ./inpe_deter_brazil_producer_data ./inpe_deter_brazil_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./inpe_deter_brazil_producer_kafka_producer/tests ./inpe_deter_brazil_producer_data/tests