.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./ireland_opw_waterlevel_mqtt_producer_data ./ireland_opw_waterlevel_mqtt_producer_mqtt_client

install: build
	cd ireland_opw_waterlevel_mqtt_producer_data && poetry install
	cd ireland_opw_waterlevel_mqtt_producer_mqtt_client && poetry install
	pip install ./ireland_opw_waterlevel_mqtt_producer_data ./ireland_opw_waterlevel_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./ireland_opw_waterlevel_mqtt_producer_mqtt_client/tests ./ireland_opw_waterlevel_mqtt_producer_data/tests