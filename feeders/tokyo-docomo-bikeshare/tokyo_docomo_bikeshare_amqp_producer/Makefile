.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./tokyo_docomo_bikeshare_amqp_producer_data ./tokyo_docomo_bikeshare_amqp_producer_amqp_producer

install: build
	cd tokyo_docomo_bikeshare_amqp_producer_data && poetry install
	cd tokyo_docomo_bikeshare_amqp_producer_amqp_producer && poetry install
	pip install ./tokyo_docomo_bikeshare_amqp_producer_data ./tokyo_docomo_bikeshare_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./tokyo_docomo_bikeshare_amqp_producer_amqp_producer/tests ./tokyo_docomo_bikeshare_amqp_producer_data/tests
