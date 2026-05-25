.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./eaws_albina_amqp_producer_data ./eaws_albina_amqp_producer_amqp_producer

install: build
	cd eaws_albina_amqp_producer_data && poetry install
	cd eaws_albina_amqp_producer_amqp_producer && poetry install
	pip install ./eaws_albina_amqp_producer_data ./eaws_albina_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./eaws_albina_amqp_producer_amqp_producer/tests ./eaws_albina_amqp_producer_data/tests
