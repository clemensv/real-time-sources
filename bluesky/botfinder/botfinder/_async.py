"""Asyncio helper that works both in plain Python and inside Jupyter/Fabric
notebooks (where an event loop is already running).
"""

from __future__ import annotations

import asyncio
from typing import Any, Coroutine


def run_async(coro: Coroutine[Any, Any, Any]) -> Any:
    """Run ``coro`` to completion and return its result.

    - If no event loop is running (CLI / scripts), uses :func:`asyncio.run`.
    - If a loop is already running (Jupyter / Fabric notebooks), executes the
      coroutine on a fresh loop in a worker thread to avoid the
      ``asyncio.run() cannot be called from a running event loop`` error.
    """
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    import threading

    result: dict[str, Any] = {}

    def _runner() -> None:
        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)
            result["value"] = loop.run_until_complete(coro)
        except BaseException as exc:  # noqa: BLE001 - re-raised below
            result["error"] = exc
        finally:
            loop.close()

    thread = threading.Thread(target=_runner, daemon=True)
    thread.start()
    thread.join()

    if "error" in result:
        raise result["error"]
    return result["value"]
