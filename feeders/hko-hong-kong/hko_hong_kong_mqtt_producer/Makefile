.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./hko_hong_kong_mqtt_producer_data ./hko_hong_kong_mqtt_producer_mqtt_client

install: build
	cd hko_hong_kong_mqtt_producer_data && poetry install
	cd hko_hong_kong_mqtt_producer_mqtt_client && poetry install
	pip install ./hko_hong_kong_mqtt_producer_data ./hko_hong_kong_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./hko_hong_kong_mqtt_producer_mqtt_client/tests ./hko_hong_kong_mqtt_producer_data/tests