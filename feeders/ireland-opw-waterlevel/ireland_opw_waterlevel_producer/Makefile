.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./ireland_opw_waterlevel_producer_data ./ireland_opw_waterlevel_producer_kafka_producer

install: build
	cd ireland_opw_waterlevel_producer_data && poetry install
	cd ireland_opw_waterlevel_producer_kafka_producer && poetry install
	pip install ./ireland_opw_waterlevel_producer_data ./ireland_opw_waterlevel_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./ireland_opw_waterlevel_producer_kafka_producer/tests ./ireland_opw_waterlevel_producer_data/tests