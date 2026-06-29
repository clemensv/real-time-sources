.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./hsl_hfp_upstream_data ./hsl_hfp_upstream_mqtt_client

install: build
	cd hsl_hfp_upstream_data && poetry install
	cd hsl_hfp_upstream_mqtt_client && poetry install
	pip install ./hsl_hfp_upstream_data ./hsl_hfp_upstream_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./hsl_hfp_upstream_mqtt_client/tests ./hsl_hfp_upstream_data/tests