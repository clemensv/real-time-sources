"""
Mode-S Data Poller
Polls Mode-S data from dump1090 and sends it to a Kafka topic using SASL PLAIN authentication.
"""

import os
import json
import signal
import sys
import asyncio
import threading
import aiohttp
import re
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, AsyncIterator, Any
from zoneinfo import ZoneInfo
import argparse
import math
import pyModeS as pms
from pyModeS.extra.tcpclient import TcpClient
from mode_s_producer_data.mode_s.modes_adsb_record import ModeS_ADSB_Record
from mode_s_producer_data.mode_s.messages import Messages
from mode_s_producer_kafka_producer.producer import ModeSEventProducer
from collections import deque
from confluent_kafka import Producer

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


class ADSBClient(TcpClient):
    def __init__(self, host, port, producer: ModeSEventProducer, rawtype='beast', ref_lat=0, ref_lon=0, stationid='station1'):
        super(ADSBClient, self).__init__(host, port, rawtype)
        self.ref_lat = ref_lat
        self.ref_lon = ref_lon
        self.producer = producer
        self.stationid = stationid
        self.messages_since_last_flush = 0
        self.records_since_last_flush = 0
        self.task_queue = deque()

    def stop(self):
        self.stop_flag = True
        return super().stop()
    
    def handle_messages(self, messages):
        if self.stop_flag:
            return
        msgs = []
        for msg, ts in messages:
            raw_msg = bytes.fromhex(msg)
            if len(raw_msg) < 7:
                continue
            ts_ms = int(ts * 1000)
            df = pms.df(msg)
            icao = pms.icao(msg)
            dbfs_rssi = None
            raw_rssi = raw_msg[6]
            if raw_rssi > 0:
                rssi_ratio = raw_rssi / 255
                signal_level = rssi_ratio ** 2
                dbfs_rssi = round(10 * math.log10(signal_level), 2)

            record = ModeS_ADSB_Record(
                ts=ts_ms, icao=icao, df=df, rssi=dbfs_rssi, tc=None, bcode=None, alt=None, cs=None, sq=None, lat=None, lon=None, 
                spd=None, ang=None, vr=None, spd_type=None, dir_src=None, vr_src=None, ws=None, wd=None, at=None, ap=None, hm=None, 
                roll=None, trak=None, gs=None, tas=None, hd=None, ias=None, m=None, vrb=None, vri=None, emst=None, tgt=None, opst=None
            )
            if df in (17, 18):
                if pms.crc(msg) != 0:
                    continue
                tc = pms.typecode(msg)
                record.tc = tc
                if 1 <= tc <= 4:
                    record.cs = pms.adsb.callsign(msg)
                elif 5 <= tc <= 8:
                    lat, lon = pms.adsb.surface_position_with_ref(msg, self.ref_lat, self.ref_lon)
                    record.lat, record.lon = lat, lon
                elif 9 <= tc <= 18:
                    record.alt = pms.adsb.altitude(msg)
                    lat, lon = pms.adsb.airborne_position_with_ref(msg, self.ref_lat, self.ref_lon)
                    record.lat, record.lon = lat, lon
                elif tc == 19:
                    speed, angle, vr, spd_type, *extras = pms.adsb.velocity(msg)
                    record.spd, record.ang, record.vr = speed, angle, vr
                    record.spd_type = spd_type
                    if len(extras) > 0:
                        record.dir_src = extras[0]
                    if len(extras) > 1:
                        record.vr_src = extras[1]
                elif 20 <= tc <= 22:
                    record.alt = pms.adsb.altitude(msg)
                    lat, lon = pms.adsb.airborne_position_with_ref(msg, self.ref_lat, self.ref_lon)
                    record.lat, record.lon = lat, lon
            elif df in (20, 21):
                bds = pms.bds.infer(msg, mrar=True)
                record.bcode = bds if bds else None
                if df == 20:
                    record.alt = pms.common.altcode(msg)
                if df == 21:
                    record.sq = str(pms.common.idcode(msg))
                if bds == "BDS44":
                    ws, wd = pms.commb.wind44(msg)
                    record.ws, record.wd = ws, wd
                    record.at = pms.commb.temp44(msg)
                    record.ap = pms.commb.p44(msg)
                    record.hm = pms.commb.hum44(msg)
                elif bds == "BDS50":
                    record.roll = pms.commb.roll50(msg)
                    record.trak = pms.commb.trk50(msg)
                    record.gs = pms.commb.gs50(msg)
                    record.tas = pms.commb.tas50(msg)
                elif bds == "BDS60":
                    record.hd = pms.commb.hdg60(msg)
                    record.ias = pms.commb.ias60(msg)
                    record.m = pms.commb.mach60(msg)
                    record.vrb = pms.commb.vr60baro(msg)
                    record.vri = pms.commb.vr60ins(msg)
            msgs.append(record)

        if len(msgs) > 0:
            bundle = Messages(messages=msgs)
            self.task_queue.append(bundle)
            if len(self.task_queue) > 20:
                logger.warning("Queue length is now %d", len(self.task_queue))


    async def queue_consumer(self, stop_event: threading.Event):
        try:
            last_flush = datetime.now()
            last_info_log = datetime.now()
            messages_since_last_log = 0
            records_since_last_log = 0
            while stop_event.is_set() is False:
                if self.task_queue:
                    try:
                        bundle:Messages = self.task_queue.popleft()
                        self.messages_since_last_flush += 1
                        self.records_since_last_flush += len(bundle.messages)
                        messages_since_last_log += 1
                        records_since_last_log += len(bundle.messages)
                        await self.producer.send_mode_s_messages(
                            _stationid=self.stationid,
                            data=bundle,
                            content_type="application/json",
                            flush_producer=False
                        )
                        if (datetime.now() - last_flush) > timedelta(seconds=1) or self.records_since_last_flush >= 1000:
                            if last_info_log < datetime.now() - timedelta(minutes=5):
                                logging.info("Messages %d, records %d, queue length is %d", messages_since_last_log, records_since_last_log, len(self.task_queue))
                                last_info_log = datetime.now()
                                messages_since_last_log = 0
                                records_since_last_log = 0
                            else:
                                logging.debug("Flushing producer, messages %d, records %d, queue length is %d", self.messages_since_last_flush, self.records_since_last_flush, len(self.task_queue))
                            self.producer.producer.flush()
                            self.messages_since_last_flush = 0
                            self.records_since_last_flush = 0
                            last_flush = datetime.now()
                    except asyncio.CancelledError:
                        logging.info("Queue consumer task cancelled")
                        return
                    except Exception as e:
                        logging.error("Error sending messages: %s", e)
                else:
                    await asyncio.sleep(0.05)
        except asyncio.CancelledError:
            logging.info("Queue consumer task cancelled")
            return
        except Exception as e:
            logging.error("Queue consumer task error: %s", e)
            raise e


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """
    Parse the connection string and extract bootstrap server, topic name, username, and password.
    """
    config_dict = {
        'sasl.username': '$ConnectionString',
        'sasl.password': connection_string.strip(),
    }
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part:
                endpoint = part.split('=')[1].replace('sb://', '')
                endpoint = endpoint.rstrip('/')
                if ':' not in endpoint:
                    endpoint += ':9093'
                config_dict['bootstrap.servers'] = endpoint
            elif 'EntityPath' in part:
                config_dict['kafka_topic'] = part.split('=')[1]
    except IndexError as e:
        raise ValueError("Invalid connection string format") from e
    return config_dict

async def main():
    parser = argparse.ArgumentParser(description="Mode-S ADS-B Client")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")
    feed_parser = subparsers.add_parser('feed', help="Poll ADS-B data and feed it to Kafka")

    feed_parser.add_argument('--host', type=str, default=os.environ.get('DUMP1090_HOST'),
                             help="Dump1090 host (default from DUMP1090_HOST)")
    feed_parser.add_argument('--port', type=int, default=os.environ.get('DUMP1090_PORT'),
                             help="Dump1090 port (default from DUMP1090_PORT)")
    feed_parser.add_argument('--ref-lat', type=float, default=os.environ.get('REF_LAT'),
                             help="Reference latitude (default from REF_LAT)")
    feed_parser.add_argument('--ref-lon', type=float, default=os.environ.get('REF_LON'),
                             help="Reference longitude (default from REF_LON)")
    feed_parser.add_argument('--stationid', type=str, default=os.environ.get('STATIONID', 'station1'),
                             help="Station ID (default from STATIONID)")

    feed_parser.add_argument('--connection-string', type=str, default=os.environ.get('CONNECTION_STRING'),
                             help="Kafka connection string (default from CONNECTION_STRING)")

    feed_parser.add_argument('--kafka-bootstrap-servers', type=str,
                             default=os.environ.get('KAFKA_BOOTSTRAP_SERVERS'),
                             help="Kafka servers (default from KAFKA_BOOTSTRAP_SERVERS)")
    feed_parser.add_argument('--kafka-topic', type=str,
                             default=os.environ.get('KAFKA_TOPIC'),
                             help="Kafka topic (default from KAFKA_TOPIC)")
    feed_parser.add_argument('--sasl-username', type=str,
                             default=os.environ.get('SASL_USERNAME'),
                             help="SASL username (default from SASL_USERNAME)")
    feed_parser.add_argument('--sasl-password', type=str,
                             default=os.environ.get('SASL_PASSWORD'),
                             help="SASL password (default from SASL_PASSWORD)")

    feed_parser.add_argument('--content-mode', type=str, choices=['structured','binary'], default='structured',
                             help="CloudEvent content mode")

    args = parser.parse_args()
    if args.subcommand == 'feed':
        # Host/port/pos checks
        if not args.host:
            print("Error: Dump1090 host is required (env: DUMP1090_HOST or --host)")
            return
        if not args.port:
            print("Error: Dump1090 port is required (env: DUMP1090_PORT or --port)")
            return
        if args.ref_lat is None:
            print("Error: Antenna latitude is required (env: REF_LAT or --ref-lat)")
            return
        if args.ref_lon is None:
            print("Error: Antenna longitude is required (env: REF_LON or --ref-lon)")
            return

        # Kafka parameter handling
        kafka_bootstrap_servers = None
        kafka_topic = None
        sasl_username = None
        sasl_password = None

        if args.connection_string:
            config_params = parse_connection_string(args.connection_string)
            kafka_bootstrap_servers = config_params.get('bootstrap.servers')
            kafka_topic = config_params.get('kafka_topic')
            sasl_username = config_params.get('sasl.username')
            sasl_password = config_params.get('sasl.password')
        else:
            kafka_bootstrap_servers = args.kafka_bootstrap_servers
            kafka_topic = args.kafka_topic
            sasl_username = args.sasl_username
            sasl_password = args.sasl_password

        if not kafka_bootstrap_servers:
            print("Error: No Kafka bootstrap servers found.")
            return
        if not kafka_topic:
            print("Error: No Kafka topic found.")
            return
        if not sasl_username or not sasl_password:
            print("Error: SASL username and password are required.")
            return

        # Build Producer
        kafka_config = {
            'bootstrap.servers': kafka_bootstrap_servers,
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'SASL_SSL',
            'sasl.username': sasl_username,
            'sasl.password': sasl_password
        }
        kafka_producer = Producer(kafka_config)
        producer = ModeSEventProducer(kafka_producer, topic=kafka_topic, content_mode=args.content_mode)

        client = ADSBClient(
            host=args.host,
            port=args.port,
            producer=producer,
            rawtype='beast',
            ref_lat=args.ref_lat,
            ref_lon=args.ref_lon,
            stationid=args.stationid
        )

        stop_event = threading.Event()

        def signal_handler(signum, frame):
            stop_event.set()

        signal.signal(signal.SIGINT, signal_handler)

        try:
            # Run client.run as a regular thread
            run_thread = threading.Thread(target=client.run)
            run_thread.start()
            await client.queue_consumer(stop_event)
            client.stop()
            
        except KeyboardInterrupt:
            print("Interrupted")
        except Exception as e:
            print("Error: %s" % e)


if __name__ == "__main__":
    asyncio.run(main())
