.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./usgs_nwis_wq_amqp_producer_data ./usgs_nwis_wq_amqp_producer_amqp_producer

install: build
	cd usgs_nwis_wq_amqp_producer_data && poetry install
	cd usgs_nwis_wq_amqp_producer_amqp_producer && poetry install
	pip install ./usgs_nwis_wq_amqp_producer_data ./usgs_nwis_wq_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./usgs_nwis_wq_amqp_producer_amqp_producer/tests ./usgs_nwis_wq_amqp_producer_data/tests
