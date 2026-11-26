"""Entrypoint shared by independently packaged transport applications."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
from pathlib import Path
import signal

from usgs_waterdata_core import WaterDataClient
from usgs_waterdata_core.state import DeliveryState

from .poller import NativePoller


def boolean(value: str) -> bool:
    if value.lower() not in {"true", "false", "1", "0", "yes", "no"}:
        raise ValueError(f"Expected a boolean, got {value!r}")
    return value.lower() in {"true", "1", "yes"}


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Publish native USGS Water Data continuous observations.")
    result.add_argument("command", choices=["feed"], nargs="?", default="feed")
    result.add_argument("--sites", default=os.getenv("USGS_WATERDATA_SITES", "USGS-01646500"),
                        help="Comma-separated monitoring-location IDs; numeric USGS site numbers also accepted.")
    result.add_argument("--parameters", default=os.getenv("USGS_WATERDATA_PARAMETERS", "00010,00060"),
                        help="Comma-separated five-digit parameter codes; empty selects all continuous parameters.")
    result.add_argument("--polling-interval", type=float, default=float(os.getenv("POLLING_INTERVAL", "300")),
                        help="Seconds between polling cycles, default 300.")
    result.add_argument("--state-file", default=os.getenv("STATE_FILE", ""),
                        help="Atomic delivery checkpoint file; empty uses memory only.")
    result.add_argument("--once", action="store_true", default=boolean(os.getenv("ONCE_MODE", "false")),
                        help="Run one complete polling cycle and exit nonzero on any failed slice.")
    result.add_argument("--lookback-hours", type=float, default=float(os.getenv("USGS_WATERDATA_LOOKBACK_HOURS", "2")),
                        help="Initial/recent observation window in hours, default two.")
    result.add_argument("--reference-interval", type=float, default=float(os.getenv("USGS_WATERDATA_REFERENCE_INTERVAL", "86400")),
                        help="Seconds between full reference refreshes.")
    result.add_argument("--overlap-seconds", type=float, default=float(os.getenv("USGS_WATERDATA_OVERLAP_SECONDS", "300")),
                        help="Overlap on last_modified correction windows; corrections have no observation-time filter.")
    return result


async def run(args: argparse.Namespace, transport: str) -> None:
    from .transports import open_sink

    sites = list(dict.fromkeys(
        site.strip() if "-" in site else f"USGS-{site.strip()}"
        for site in args.sites.split(",") if site.strip()
    ))
    if not sites or min(args.polling_interval, args.lookback_hours, args.reference_interval, args.overlap_seconds) <= 0:
        raise ValueError("Provide sites and positive polling/reference/lookback/overlap intervals")
    state = DeliveryState(Path(args.state_file) if args.state_file else None)
    with WaterDataClient() as client:
        sink = await open_sink(transport)
        try:
            poller = NativePoller(
                client, sink, state, sites=sites, parameters=args.parameters,
                lookback_hours=args.lookback_hours, reference_interval=args.reference_interval,
                overlap_seconds=args.overlap_seconds,
            )
            task = asyncio.create_task(poller.run(args.polling_interval, args.once))
            loop = asyncio.get_running_loop()
            prior_handlers = {}

            def stop(signum, frame):
                loop.call_soon_threadsafe(task.cancel)

            import threading
            if threading.current_thread() is threading.main_thread():
                for signum in (signal.SIGINT, signal.SIGTERM):
                    prior_handlers[signum] = signal.signal(signum, stop)
            try:
                await task
            except asyncio.CancelledError:
                logging.info("Stopping USGS native feeder")
            finally:
                for signum, handler in prior_handlers.items():
                    signal.signal(signum, handler)
        finally:
            await sink.close()


def main(transport: str = "kafka") -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(),
                        format="%(asctime)s %(levelname)s %(name)s %(message)s")
    logging.info("USGS Water Data native feeder 0.1.0; transport=%s", transport)
    asyncio.run(run(parser().parse_args(), transport))
