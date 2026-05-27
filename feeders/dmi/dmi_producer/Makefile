.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./dmi_producer_data ./dmi_producer_kafka_producer

install: build
	cd dmi_producer_data && poetry install
	cd dmi_producer_kafka_producer && poetry install
	pip install ./dmi_producer_data ./dmi_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./dmi_producer_kafka_producer/tests ./dmi_producer_data/tests