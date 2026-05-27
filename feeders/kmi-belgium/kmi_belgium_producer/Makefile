.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./kmi_belgium_producer_data ./kmi_belgium_producer_kafka_producer

install: build
	cd kmi_belgium_producer_data && poetry install
	cd kmi_belgium_producer_kafka_producer && poetry install
	pip install ./kmi_belgium_producer_data ./kmi_belgium_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./kmi_belgium_producer_kafka_producer/tests ./kmi_belgium_producer_data/tests