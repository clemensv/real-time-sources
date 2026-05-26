.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./waterinfo_vmm_amqp_producer_data ./waterinfo_vmm_amqp_producer_amqp_producer

install: build
	cd waterinfo_vmm_amqp_producer_data && poetry install
	cd waterinfo_vmm_amqp_producer_amqp_producer && poetry install
	pip install ./waterinfo_vmm_amqp_producer_data ./waterinfo_vmm_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./waterinfo_vmm_amqp_producer_amqp_producer/tests ./waterinfo_vmm_amqp_producer_data/tests
