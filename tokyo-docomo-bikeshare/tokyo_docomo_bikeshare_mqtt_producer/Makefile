.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./tokyo_docomo_bikeshare_mqtt_producer_data ./tokyo_docomo_bikeshare_mqtt_producer_mqtt_client

install: build
	cd tokyo_docomo_bikeshare_mqtt_producer_data && poetry install
	cd tokyo_docomo_bikeshare_mqtt_producer_mqtt_client && poetry install
	pip install ./tokyo_docomo_bikeshare_mqtt_producer_data ./tokyo_docomo_bikeshare_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./tokyo_docomo_bikeshare_mqtt_producer_mqtt_client/tests ./tokyo_docomo_bikeshare_mqtt_producer_data/tests