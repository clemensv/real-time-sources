.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./wikimedia_osm_diffs_mqtt_producer_data ./wikimedia_osm_diffs_mqtt_producer_mqtt_client

install: build
	cd wikimedia_osm_diffs_mqtt_producer_data && poetry install
	cd wikimedia_osm_diffs_mqtt_producer_mqtt_client && poetry install
	pip install ./wikimedia_osm_diffs_mqtt_producer_data ./wikimedia_osm_diffs_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./wikimedia_osm_diffs_mqtt_producer_mqtt_client/tests ./wikimedia_osm_diffs_mqtt_producer_data/tests