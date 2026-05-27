.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./irceline_belgium_producer_data ./irceline_belgium_producer_kafka_producer

install: build
	cd irceline_belgium_producer_data && poetry install
	cd irceline_belgium_producer_kafka_producer && poetry install
	pip install ./irceline_belgium_producer_data ./irceline_belgium_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./irceline_belgium_producer_kafka_producer/tests ./irceline_belgium_producer_data/tests