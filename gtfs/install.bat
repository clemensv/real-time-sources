pushd %~dp0
pip install -e gtfs_rt_producer\gtfs_rt_producer_data
pip install -e gtfs_rt_producer\gtfs_rt_producer_kafka_producer
pip install -e .\gtfs_rt_bridge
popd