.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./airqo_uganda_producer_data ./airqo_uganda_producer_kafka_producer

install: build
	cd airqo_uganda_producer_data && poetry install
	cd airqo_uganda_producer_kafka_producer && poetry install
	pip install ./airqo_uganda_producer_data ./airqo_uganda_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./airqo_uganda_producer_kafka_producer/tests ./airqo_uganda_producer_data/tests