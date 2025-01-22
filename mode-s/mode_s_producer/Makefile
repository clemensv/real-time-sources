.PHONY: build install

build:
	pip install wheel poetry
	pip wheel -w whl ./mode_s_producer_data ./mode_s_producer_kafka_producer

install: build
	poetry export --only dev -f requirements.txt -o requirements_mode_s_producer_data_dev.txt -C mode_s_producer_data
	poetry export --only dev -f requirements.txt -o requirements_mode_s_producer_kafka_producer_dev.txt -C mode_s_producer_kafka_producer
	pip install -r requirements_mode_s_producer_data_dev.txt
	pip install -r requirements_mode_s_producer_kafka_producer_dev.txt
	pip install ./mode_s_producer_data ./mode_s_producer_kafka_producer

test: install
	pytest ./mode_s_producer_kafka_producer/tests ./mode_s_producer_data/tests