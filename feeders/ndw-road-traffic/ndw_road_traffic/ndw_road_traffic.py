"""NDW Netherlands Road Traffic bridge — Kafka transport.







Polls gzip-compressed DATEX II XML files from the Dutch NDW open-data



platform and emits CloudEvents for traffic speed, travel time, situations,



DRIP, and MSI sign data onto Kafka topics.







Transport-neutral parsing/state/acquisition logic lives in



ndw_road_traffic_core.ndw_road_traffic.



"""







from __future__ import annotations







import argparse



import logging



import os



import sys



import time



from typing import Any, Dict, List, Optional, Tuple







from confluent_kafka import Producer







from ndw_road_traffic_producer_data import (



    PointMeasurementSite,



    RouteMeasurementSite,



    TrafficObservation,



    TravelTimeObservation,



    DripSign,



    DripDisplayState,



    MsiSign,



    MsiDisplayState,



    Roadwork,



    BridgeOpening,



    TemporaryClosure,



    TemporarySpeedLimit,



    SafetyRelatedMessage,



)



from ndw_road_traffic_producer_kafka_producer.producer import (



    NLNDWAVGEventProducer,



    NLNDWDRIPEventProducer,



    NLNDWMSIEventProducer,



    NLNDWSituationsEventProducer,



)



import ndw_road_traffic_core.ndw_road_traffic_core.ndw_road_traffic as _ndw_core

from ndw_road_traffic_core.ndw_road_traffic import (



    BASE_URL,



    DATEX2_V2,



    SITUATION_FEEDS,



    DEFAULT_TOPIC,



    DEFAULT_POLL_INTERVAL_SECONDS,



    DEFAULT_REFERENCE_REFRESH_SECONDS,



    DEFAULT_SITUATION_INTERVAL_SECONDS,



    DEFAULT_STATE_FILE,



    REFERENCE_FLUSH_BATCH_SIZE,



    DEFAULT_MAX_RECORDS_PER_FAMILY,



    StateManager,



    NdwAcquirer,



    parse_traffic_speed_xml,



    parse_travel_time_xml,



    parse_measurement_site_xml,



    parse_drip_xml,



    parse_msi_xml,



    parse_situation_xml,



)







if sys.gettrace() is not None:



    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")



else:



    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")







logger = logging.getLogger(__name__)

download_gzip_xml = _ndw_core.download_gzip_xml











# ---------------------------------------------------------------------------



# Connection string / Kafka helpers



# ---------------------------------------------------------------------------







def parse_connection_string(connection_string: str) -> Dict[str, str]:



    config_dict: Dict[str, str] = {}



    try:



        for part in connection_string.split(";"):



            if "Endpoint" in part:



                config_dict["bootstrap.servers"] = (



                    part.split("=", 1)[1].strip('"').replace("sb://", "").replace("/", "") + ":9093"



                )



            elif "EntityPath" in part:



                config_dict["entity_path"] = part.split("=", 1)[1].strip('"')



            elif "SharedAccessKeyName" in part:



                config_dict["sasl.username"] = part.split("=", 1)[1].strip('"')



            elif "SharedAccessKey" in part:



                config_dict["sasl.password"] = part.split("=", 1)[1].strip('"')



    except (IndexError, ValueError) as exc:



        raise ValueError("Invalid connection string format") from exc



    return config_dict











def _build_kafka_config(connection_string: str, enable_tls: bool = True) -> Tuple[Dict[str, str], Optional[str]]:



    topic: Optional[str] = None







    if "BootstrapServer=" in connection_string:



        parts: Dict[str, str] = {}



        for part in connection_string.split(";"):



            if "=" in part:



                k, v = part.split("=", 1)



                parts[k.strip()] = v.strip().strip('"')



        config: Dict[str, str] = {"bootstrap.servers": parts.get("BootstrapServer", "")}



        topic = parts.get("EntityPath")



    else:



        parsed = parse_connection_string(connection_string)



        config = {



            "bootstrap.servers": parsed.get("bootstrap.servers", ""),



            "security.protocol": "SASL_SSL",



            "sasl.mechanisms": "PLAIN",



            "sasl.username": "$ConnectionString",



            "sasl.password": connection_string.strip(),



        }



        topic = parsed.get("entity_path")







    if not enable_tls and "security.protocol" not in config:



        config["security.protocol"] = "PLAINTEXT"







    return config, topic











class _DryRunProducer:



    """Minimal producer used for local upstream fetch/parse validation."""







    def __init__(self) -> None:



        self.message_count = 0







    def produce(self, *args: Any, **kwargs: Any) -> None:



        self.message_count += 1







    def flush(self, timeout: Optional[float] = None) -> int:



        return 0











# ---------------------------------------------------------------------------



# Poller (Kafka transport)



# ---------------------------------------------------------------------------







class NdwPoller:



    def __init__(



        self,



        avg_producer: NLNDWAVGEventProducer,



        drip_producer: NLNDWDRIPEventProducer,



        msi_producer: NLNDWMSIEventProducer,



        situations_producer: NLNDWSituationsEventProducer,



        state: StateManager,



        poll_interval: int = DEFAULT_POLL_INTERVAL_SECONDS,



        reference_refresh_interval: int = DEFAULT_REFERENCE_REFRESH_SECONDS,



        situation_interval: int = DEFAULT_SITUATION_INTERVAL_SECONDS,



        base_url: str = BASE_URL,



        max_records_per_family: Optional[int] = DEFAULT_MAX_RECORDS_PER_FAMILY,



    ):



        self.avg_producer = avg_producer



        self.drip_producer = drip_producer



        self.msi_producer = msi_producer



        self.situations_producer = situations_producer



        self.state = state



        self.poll_interval = poll_interval



        self.reference_refresh_interval = reference_refresh_interval



        self.situation_interval = situation_interval



        self.acquirer = NdwAcquirer(base_url=base_url, max_records_per_family=max_records_per_family)







        self._last_reference_emit: float = 0



        self._last_situation_poll: float = 0







    def _sync_core_download_alias(self) -> None:
        _ndw_core.download_gzip_xml = download_gzip_xml
        _ndw_core.parse_measurement_site_xml = parse_measurement_site_xml
        _ndw_core.parse_traffic_speed_xml = parse_traffic_speed_xml
        _ndw_core.parse_travel_time_xml = parse_travel_time_xml
        _ndw_core.parse_drip_xml = parse_drip_xml
        _ndw_core.parse_msi_xml = parse_msi_xml
        _ndw_core.parse_situation_xml = parse_situation_xml

    def _flush_and_check(self, producer_obj: Any) -> bool:



        remainder = producer_obj.producer.flush(timeout=60)



        if remainder != 0:



            logger.warning("Kafka flush had %d undelivered messages", remainder)



            return False



        return True







    def _flush_reference_batch(self, producer_obj: Any, count: int, label: str) -> bool:



        if count and count % REFERENCE_FLUSH_BATCH_SIZE == 0:



            if not self._flush_and_check(producer_obj):



                logger.warning(



                    "Flush failed for %s after %d queued reference records; keeping old cache",



                    label, count,



                )



                return False



        return True







    def emit_reference_data(self) -> None:

        self._sync_core_download_alias()



        logger.info("Fetching reference data (measurement sites, DRIP signs, MSI signs)")



        self._refresh_measurement_sites()



        self._refresh_drip_signs()



        self._refresh_msi_signs()



        self._last_reference_emit = time.time()







    def _refresh_measurement_sites(self) -> None:
        self._sync_core_download_alias()



        try:



            new_point, new_route = self.acquirer.fetch_measurement_sites()



        except Exception:



            logger.exception("Failed to fetch/parse measurement site data")



            return







        count = 0



        for rec in new_point:



            data = PointMeasurementSite(



                measurement_site_id=rec["measurement_site_id"],



                name=rec["name"],



                measurement_site_type=rec["measurement_site_type"],



                period=rec["period"],



                latitude=rec["latitude"],



                longitude=rec["longitude"],



                road_name=rec["road_name"],



                lane_count=rec["lane_count"],



                carriageway_type=rec["carriageway_type"],



            )



            self.avg_producer.send_nl_ndw_avg_point_measurement_site(



                rec["measurement_site_id"], data, flush_producer=False



            )



            count += 1



            if not self._flush_reference_batch(self.avg_producer, count, "PointMeasurementSite"):



                return







        if count:



            if self._flush_and_check(self.avg_producer):



                logger.info("Emitted %d PointMeasurementSite reference events", count)



            else:



                logger.warning("Flush failed for PointMeasurementSite")



        else:



            logger.info("No point measurement sites found in feed")







        count = 0



        for rec in new_route:



            data = RouteMeasurementSite(



                measurement_site_id=rec["measurement_site_id"],



                name=rec["name"],



                measurement_site_type=rec["measurement_site_type"],



                period=rec["period"],



                start_latitude=rec["start_latitude"],



                start_longitude=rec["start_longitude"],



                end_latitude=rec["end_latitude"],



                end_longitude=rec["end_longitude"],



                road_name=rec["road_name"],



                length_metres=rec["length_metres"],



            )



            self.avg_producer.send_nl_ndw_avg_route_measurement_site(



                rec["measurement_site_id"], data, flush_producer=False



            )



            count += 1



            if not self._flush_reference_batch(self.avg_producer, count, "RouteMeasurementSite"):



                return







        if count:



            if self._flush_and_check(self.avg_producer):



                logger.info("Emitted %d RouteMeasurementSite reference events", count)



            else:



                logger.warning("Flush failed for RouteMeasurementSite")







    def _refresh_drip_signs(self) -> None:
        self._sync_core_download_alias()



        try:



            new_signs, _ = self.acquirer.fetch_drip()



        except Exception:



            logger.exception("Failed to fetch/parse DRIP sign data")



            return







        count = 0



        for rec in new_signs:



            data = DripSign(



                vms_controller_id=rec["vms_controller_id"],



                vms_index=rec["vms_index"],



                vms_type=rec["vms_type"],



                latitude=rec["latitude"],



                longitude=rec["longitude"],



                road_name=rec["road_name"],



                description=rec["description"],



            )



            self.drip_producer.send_nl_ndw_drip_drip_sign(



                rec["vms_controller_id"], rec["vms_index"], data, flush_producer=False



            )



            count += 1



            if not self._flush_reference_batch(self.drip_producer, count, "DripSign"):



                return







        if count:



            if self._flush_and_check(self.drip_producer):



                logger.info("Emitted %d DripSign reference events", count)



            else:



                logger.warning("Flush failed for DripSign")







    def _refresh_msi_signs(self) -> None:
        self._sync_core_download_alias()



        try:



            new_signs, _ = self.acquirer.fetch_msi()



        except Exception:



            logger.exception("Failed to fetch/parse MSI sign data")



            return







        count = 0



        for rec in new_signs:



            data = MsiSign(



                sign_id=rec["sign_id"],



                sign_type=rec["sign_type"],



                latitude=rec["latitude"],



                longitude=rec["longitude"],



                road_name=rec["road_name"],



                lane=rec["lane"],



                description=rec["description"],



            )



            self.msi_producer.send_nl_ndw_msi_msi_sign(



                rec["sign_id"], data, flush_producer=False



            )



            count += 1



            if not self._flush_reference_batch(self.msi_producer, count, "MsiSign"):



                return







        if count:



            if self._flush_and_check(self.msi_producer):



                logger.info("Emitted %d MsiSign reference events", count)



            else:



                logger.warning("Flush failed for MsiSign")







    def _poll_speed(self) -> int:
        self._sync_core_download_alias()



        try:



            records = self.acquirer.fetch_speed_observations()



        except Exception:



            logger.exception("Failed to fetch traffic speed data")



            return 0







        pending_state: Dict[str, str] = {}



        count = 0



        for rec in records:



            sid = rec["measurement_site_id"]



            mtime = rec["measurement_time"]



            if self.state.state.get("speed", {}).get(sid) == mtime:



                continue



            data = TrafficObservation(



                measurement_site_id=sid,



                measurement_time=mtime,



                average_speed=rec["average_speed"],



                vehicle_flow_rate=rec["vehicle_flow_rate"],



                number_of_lanes_with_data=rec["number_of_lanes_with_data"],



            )



            self.avg_producer.send_nl_ndw_avg_traffic_observation(



                sid, data, flush_producer=False



            )



            pending_state[sid] = mtime



            count += 1







        if count:



            if self._flush_and_check(self.avg_producer):



                self.state.state.setdefault("speed", {}).update(pending_state)



            else:



                logger.warning("Flush failed for TrafficObservation; state not advanced")



                count = 0







        logger.info("Emitted %d TrafficObservation events (of %d sites)", count, len(records))



        return count







    def _poll_traveltime(self) -> int:
        self._sync_core_download_alias()



        try:



            records = self.acquirer.fetch_traveltime_observations()



        except Exception:



            logger.exception("Failed to fetch travel time data")



            return 0







        pending_state: Dict[str, str] = {}



        count = 0



        for rec in records:



            sid = rec["measurement_site_id"]



            mtime = rec["measurement_time"]



            if self.state.state.get("traveltime", {}).get(sid) == mtime:



                continue



            data = TravelTimeObservation(



                measurement_site_id=sid,



                measurement_time=mtime,



                duration=rec["duration"],



                reference_duration=rec["reference_duration"],



                accuracy=rec["accuracy"],



                data_quality=rec["data_quality"],



                number_of_input_values=rec["number_of_input_values"],



            )



            self.avg_producer.send_nl_ndw_avg_travel_time_observation(



                sid, data, flush_producer=False



            )



            pending_state[sid] = mtime



            count += 1







        if count:



            if self._flush_and_check(self.avg_producer):



                self.state.state.setdefault("traveltime", {}).update(pending_state)



            else:



                logger.warning("Flush failed for TravelTimeObservation; state not advanced")



                count = 0







        logger.info("Emitted %d TravelTimeObservation events (of %d sites)", count, len(records))



        return count







    def _poll_drip_states(self) -> int:
        self._sync_core_download_alias()



        try:



            _, states = self.acquirer.fetch_drip()



        except Exception:



            logger.exception("Failed to fetch DRIP display states")



            return 0







        pending_state: Dict[str, str] = {}



        count = 0



        for rec in states:



            key = f"{rec['vms_controller_id']}/{rec['vms_index']}"



            pub_time = rec["publication_time"]



            if self.state.state.get("drip", {}).get(key) == pub_time:



                continue



            data = DripDisplayState(



                vms_controller_id=rec["vms_controller_id"],



                vms_index=rec["vms_index"],



                publication_time=pub_time,



                active=rec["active"],



                vms_text=rec["vms_text"],



                pictogram_code=rec["pictogram_code"],



                state=rec["state"],



            )



            self.drip_producer.send_nl_ndw_drip_drip_display_state(



                rec["vms_controller_id"], rec["vms_index"], data, flush_producer=False



            )



            pending_state[key] = pub_time



            count += 1







        if count:



            if self._flush_and_check(self.drip_producer):



                self.state.state.setdefault("drip", {}).update(pending_state)



            else:



                logger.warning("Flush failed for DripDisplayState; state not advanced")



                count = 0







        logger.info("Emitted %d DripDisplayState events", count)



        return count







    def _poll_msi_states(self) -> int:
        self._sync_core_download_alias()



        try:



            _, states = self.acquirer.fetch_msi()



        except Exception:



            logger.exception("Failed to fetch MSI display states")



            return 0







        pending_state: Dict[str, str] = {}



        count = 0



        for rec in states:



            sid = rec["sign_id"]



            pub_time = rec["publication_time"]



            if self.state.state.get("msi", {}).get(sid) == pub_time:



                continue



            data = MsiDisplayState(



                sign_id=sid,



                publication_time=pub_time,



                image_code=rec["image_code"],



                state=rec["state"],



                speed_limit=rec["speed_limit"],



            )



            self.msi_producer.send_nl_ndw_msi_msi_display_state(



                sid, data, flush_producer=False



            )



            pending_state[sid] = pub_time



            count += 1







        if count:



            if self._flush_and_check(self.msi_producer):



                self.state.state.setdefault("msi", {}).update(pending_state)



            else:



                logger.warning("Flush failed for MsiDisplayState; state not advanced")



                count = 0







        logger.info("Emitted %d MsiDisplayState events", count)



        return count







    def _poll_situations(self) -> int:
        self._sync_core_download_alias()



        total = 0



        for feed_file, feed_type in SITUATION_FEEDS:



            try:



                records = self.acquirer.fetch_situations(feed_file, feed_type)



            except Exception:



                logger.exception("Failed to fetch situation feed: %s", feed_file)



                continue







            pending_state: Dict[str, str] = {}



            count = 0



            for rec in records:



                rid = rec["situation_record_id"]



                vtime = rec["version_time"]



                if self.state.state.get("situation", {}).get(rid) == vtime:



                    continue







                try:



                    if feed_type == "roadwork":



                        data = Roadwork(



                            situation_record_id=rid,



                            version_time=vtime,



                            validity_status=rec.get("validity_status"),



                            start_time=rec.get("start_time"),



                            end_time=rec.get("end_time"),



                            road_name=rec.get("road_name"),



                            description=rec.get("description"),



                            location_description=rec.get("location_description"),



                            probability=rec.get("probability"),



                            severity=rec.get("severity"),



                            management_type=rec.get("management_type"),



                        )



                        self.situations_producer.send_nl_ndw_situations_roadwork(



                            rid, data, flush_producer=False



                        )



                    elif feed_type == "bridge_opening":



                        data = BridgeOpening(



                            situation_record_id=rid,



                            version_time=vtime,



                            validity_status=rec.get("validity_status"),



                            start_time=rec.get("start_time"),



                            end_time=rec.get("end_time"),



                            bridge_name=rec.get("bridge_name"),



                            road_name=rec.get("road_name"),



                            description=rec.get("description"),



                        )



                        self.situations_producer.send_nl_ndw_situations_bridge_opening(



                            rid, data, flush_producer=False



                        )



                    elif feed_type == "temporary_closure":



                        data = TemporaryClosure(



                            situation_record_id=rid,



                            version_time=vtime,



                            validity_status=rec.get("validity_status"),



                            start_time=rec.get("start_time"),



                            end_time=rec.get("end_time"),



                            road_name=rec.get("road_name"),



                            description=rec.get("description"),



                            location_description=rec.get("location_description"),



                            severity=rec.get("severity"),



                        )



                        self.situations_producer.send_nl_ndw_situations_temporary_closure(



                            rid, data, flush_producer=False



                        )



                    elif feed_type == "temporary_speed_limit":



                        data = TemporarySpeedLimit(



                            situation_record_id=rid,



                            version_time=vtime,



                            validity_status=rec.get("validity_status"),



                            start_time=rec.get("start_time"),



                            end_time=rec.get("end_time"),



                            road_name=rec.get("road_name"),



                            speed_limit_kmh=rec.get("speed_limit_kmh"),



                            description=rec.get("description"),



                            location_description=rec.get("location_description"),



                        )



                        self.situations_producer.send_nl_ndw_situations_temporary_speed_limit(



                            rid, data, flush_producer=False



                        )



                    elif feed_type == "safety_related_message":



                        data = SafetyRelatedMessage(



                            situation_record_id=rid,



                            version_time=vtime,



                            validity_status=rec.get("validity_status"),



                            start_time=rec.get("start_time"),



                            end_time=rec.get("end_time"),



                            road_name=rec.get("road_name"),



                            message_type=rec.get("message_type"),



                            description=rec.get("description"),



                            urgency=rec.get("urgency"),



                        )



                        self.situations_producer.send_nl_ndw_situations_safety_related_message(



                            rid, data, flush_producer=False



                        )



                except Exception:



                    logger.exception("Failed to emit situation record %s", rid)



                    continue







                pending_state[rid] = vtime



                count += 1







            if count:



                if self._flush_and_check(self.situations_producer):



                    self.state.state.setdefault("situation", {}).update(pending_state)



                    logger.info("Emitted %d %s situation events", count, feed_type)



                    total += count



                else:



                    logger.warning("Flush failed for %s situations; state not advanced", feed_type)







        return total







    def poll_cycle(self) -> None:



        now = time.time()







        if now - self._last_reference_emit >= self.reference_refresh_interval:



            self.emit_reference_data()







        self._poll_speed()



        self._poll_traveltime()



        self._poll_drip_states()



        self._poll_msi_states()







        if now - self._last_situation_poll >= self.situation_interval:



            self._poll_situations()



            self._last_situation_poll = now







        self.state.save()







    def run_forever(self) -> None:



        logger.info("Starting NDW Road Traffic poller (interval=%ds)", self.poll_interval)



        self._last_reference_emit = 0



        self._last_situation_poll = 0



        while True:



            try:



                self.poll_cycle()



            except Exception:



                logger.exception("Error during poll cycle")



            time.sleep(self.poll_interval)











# ---------------------------------------------------------------------------



# CLI entry point



# ---------------------------------------------------------------------------







def main() -> None:



    parser = argparse.ArgumentParser(description="NDW Netherlands Road Traffic bridge")



    parser.add_argument("feed_command", nargs="?", default="feed", help=argparse.SUPPRESS)



    parser.add_argument("--topic", default=None, help="Kafka topic for all messages")



    parser.add_argument("--poll-interval", type=int, default=None, help="Telemetry poll interval in seconds")



    parser.add_argument("--state-file", default=None, help="Path to state file")



    parser.add_argument("--base-url", default=os.environ.get("NDW_BASE_URL", BASE_URL), help="NDW open-data base URL")



    parser.add_argument("--once", action="store_true", help="Run one poll cycle and exit")



    parser.add_argument(



        "--dry-run",



        action="store_true",



        default=os.environ.get("DRY_RUN", "").lower() in ("1", "true", "yes"),



        help="Fetch and parse upstream data without connecting to Kafka",



    )



    args = parser.parse_args()



    if args.feed_command != "feed":



        parser.error("only the optional 'feed' command is supported")







    connection_string = os.environ.get("CONNECTION_STRING", "")



    if not connection_string and not args.dry_run:



        logger.error("CONNECTION_STRING environment variable is required")



        sys.exit(1)







    conn_topic: Optional[str] = None



    if connection_string:



        enable_tls = os.environ.get("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")



        kafka_config, conn_topic = _build_kafka_config(connection_string, enable_tls)



    else:



        kafka_config = {"bootstrap.servers": "dry-run"}







    topic = (



        conn_topic



        or args.topic



        or os.environ.get("KAFKA_TOPIC", "")



        or DEFAULT_TOPIC



    )







    poll_interval = args.poll_interval or int(



        os.environ.get("POLLING_INTERVAL", DEFAULT_POLL_INTERVAL_SECONDS)



    )



    state_file = args.state_file or os.environ.get("STATE_FILE", DEFAULT_STATE_FILE)



    max_records_per_family = os.environ.get("MAX_RECORDS_PER_FAMILY")







    producer = _DryRunProducer() if args.dry_run else Producer(kafka_config)







    avg_prod = NLNDWAVGEventProducer(producer, topic)



    drip_prod = NLNDWDRIPEventProducer(producer, topic)



    msi_prod = NLNDWMSIEventProducer(producer, topic)



    situations_prod = NLNDWSituationsEventProducer(producer, topic)







    state = StateManager(state_file)



    poller = NdwPoller(



        avg_prod,



        drip_prod,



        msi_prod,



        situations_prod,



        state,



        poll_interval,



        base_url=args.base_url.rstrip("/"),



        max_records_per_family=int(max_records_per_family) if max_records_per_family else None,



    )



    if args.once:



        logger.info("Running one NDW Road Traffic poll cycle%s", " (dry run)" if args.dry_run else "")



        poller.poll_cycle()



        if args.dry_run and isinstance(producer, _DryRunProducer):



            logger.info("Dry run queued %d CloudEvent(s)", producer.message_count)



    else:



        poller.run_forever()











if __name__ == "__main__":



    main()



