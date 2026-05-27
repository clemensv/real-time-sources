"""Async runtime bridge used by the pipeline and API helpers.

Several pipeline stages call async Bluesky HTTP helpers from synchronous
entry points such as the CLI, notebooks, or reporting code. This module
provides the compatibility shim that runs a coroutine either on the normal
event-loop-free process or on a dedicated worker-thread loop when Fabric or
Jupyter already owns the main loop.
"""

from __future__ import annotations

import asyncio
from typing import Any, Coroutine


def run_async(coro: Coroutine[Any, Any, Any]) -> Any:
    """Execute an async helper from synchronous botfinder code.
    
    Args:
        coro: Coroutine object produced by an async helper such as a Bluesky API
            fetch or co-follow graph enrichment call.
    
    Returns:
        Any: The coroutine result after it has run to completion.
    
    Notes:
        In CLI and script usage the function delegates to ``asyncio.run``. In
        Fabric notebooks and Jupyter, where a loop is already active, it spins
        up a fresh event loop in a worker thread so the rest of the pipeline can
        keep a synchronous API.
    """
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    import threading

    result: dict[str, Any] = {}

    def _runner() -> None:
        """Run the coroutine on a dedicated event loop inside the worker thread."""
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
