.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./waterinfo_vmm_producer_data ./waterinfo_vmm_producer_kafka_producer

install: build
	cd waterinfo_vmm_producer_data && poetry install
	cd waterinfo_vmm_producer_kafka_producer && poetry install
	pip install ./waterinfo_vmm_producer_data ./waterinfo_vmm_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./waterinfo_vmm_producer_kafka_producer/tests ./waterinfo_vmm_producer_data/tests