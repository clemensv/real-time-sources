

# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines

"""
Producer module for sending messages via AMQP 1.0 protocol.

Generated with Azure CBS support (target: servicebus).
Supports Entra ID (Azure AD) authentication via Claims-Based Security (CBS)
put-token, in addition to SASL PLAIN and SAS connection-string auth.
"""

import sys
import typing
import uuid
import json
import threading
import queue
import concurrent.futures
from urllib.parse import quote_plus
from proton import Message
from proton.utils import BlockingConnection
from cloudevents.http import CloudEvent
from cloudevents.conversion import to_binary, to_structured

# --- Azure CBS support (azure_cbs_target=servicebus) ---
# Two CBS auth modes are supported:
#   1. Entra ID (Azure AD) JWT bearer via an azure-identity TokenCredential
#      (``type=jwt``) -- works against live Azure Service Bus / Event Hubs.
#   2. SAS token (``type=servicebus.windows.net:sastoken``) -- works against
#      both live Azure namespaces configured for SAS and the local Service Bus
#      emulator, which validates the ``type`` field strictly and refuses JWT.
import base64
import hashlib
import hmac
import logging
import time as _cbs_time
from urllib.parse import quote
from proton import Endpoint, symbol
from proton.handlers import MessagingHandler
from proton.reactor import Container, AtLeastOnce

try:  # azure-identity is optional when only SAS auth is used
    from azure.core.credentials import TokenCredential  # type: ignore
except Exception:  # pragma: no cover - optional dep
    TokenCredential = typing.Any  # type: ignore

_cbs_logger = logging.getLogger("amqp.cbs")


class _CbsTokenProvider:
    """Abstract provider that mints a CBS put-token body + metadata."""

    token_type: str = ""

    def acquire(self) -> typing.Tuple[str, int]:
        """Return (token_body, absolute_expiry_unix_seconds)."""
        raise NotImplementedError


class _JwtTokenProvider(_CbsTokenProvider):
    """Entra ID JWT acquired from an azure-identity ``TokenCredential``."""

    token_type = "jwt"

    def __init__(self, credential, audience: str):
        self._credential = credential
        self._audience = audience

    def acquire(self) -> typing.Tuple[str, int]:
        token = self._credential.get_token(self._audience)
        return token.token, int(token.expires_on)


class _SasTokenProvider(_CbsTokenProvider):
    """SAS token minted from a shared-access key + key name.

    Produces a token of the form::

        SharedAccessSignature sr=<url-quoted resource_uri>
                              &sig=<url-quoted base64 HMAC-SHA256>
                              &se=<expiry-unix-seconds>
                              &skn=<key name>
    """

    token_type = "servicebus.windows.net:sastoken"

    def __init__(self, key_name: str, key: str, resource_uri: str,
                 ttl_seconds: int = 3600):
        if not key_name or not key:
            raise ValueError("SAS auth requires both key_name and key")
        self._key_name = key_name
        self._key = key
        self._resource_uri = resource_uri
        self._ttl = int(ttl_seconds)

    def acquire(self) -> typing.Tuple[str, int]:
        expiry = int(_cbs_time.time()) + self._ttl
        encoded_uri = quote(self._resource_uri, safe="")
        string_to_sign = (encoded_uri + "\n" + str(expiry)).encode("utf-8")
        try:
            signing_key = self._key.encode("utf-8")
        except AttributeError:
            signing_key = bytes(self._key)
        signature = base64.b64encode(
            hmac.new(signing_key, string_to_sign, hashlib.sha256).digest()
        )
        encoded_sig = quote(signature, safe="")
        token = (
            "SharedAccessSignature "
            f"sr={encoded_uri}&sig={encoded_sig}&se={expiry}"
            f"&skn={quote(self._key_name, safe='')}"
        )
        return token, expiry


class _CbsAzureHandler(MessagingHandler):
    """Reactor handler that establishes an Azure CBS-authenticated AMQP connection.

    State machine:
      1. ``on_start``                -> open SASL ANONYMOUS amqps:// connection.
      2. ``on_connection_opened``    -> attach ``$cbs`` sender + receiver pair
                                       (receiver source AND target pinned to ``$cbs``).
      3. both CBS links opened       -> send put-token request (with correlation id).
      4. CBS reply (status 200/202)  -> attach main sender to ``self._address``
                                       (with AtLeastOnce so we get accepted/rejected).
      5. main sender opened          -> signal ``_init_future`` ready.
      6. ``on_sendable`` / injected  -> drain outbound queue, track each delivery.
      7. ``on_accepted/rejected``    -> resolve the per-send ``Future``.
      8. ``on_disconnected``         -> fail everything (v1: no reconnect).
    """

    def __init__(self, host, port, address, token_provider, use_tls,
                 init_future, send_queue, close_event):
        super().__init__(auto_settle=False, auto_accept=False)
        self._host = host
        self._port = port
        self._address = address
        self._token_provider = token_provider
        self._use_tls = use_tls
        self._init_future = init_future
        self._send_queue = send_queue
        self._close_event = close_event
        self._close_requested = False

        self._container = None
        self._conn = None
        self._cbs_sender = None
        self._cbs_receiver = None
        self._main_sender = None
        self._cbs_sender_opened = False
        self._cbs_receiver_opened = False
        self._cbs_request_id = None
        self._pending: typing.Dict[bytes, concurrent.futures.Future] = {}
        self._failed = False

    # ---- lifecycle ----

    def on_start(self, event):
        self._container = event.container
        scheme = "amqps" if self._use_tls else "amqp"
        url = f"{scheme}://{self._host}:{self._port}"
        # SASL ANONYMOUS: Azure broker accepts the connection without creds;
        # authn is established by the subsequent CBS put-token exchange.
        self._conn = self._container.connect(
            url,
            sasl_enabled=True,
            allowed_mechs="ANONYMOUS",
            reconnect=False,
        )
        # Cross-thread wakeup: poll the send-queue + close-flag periodically.
        # EventInjector is not portable on Windows (needs a real socketpair),
        # so a 25ms recurring timer is used instead. Latency overhead is
        # negligible for non-bulk workloads.
        self._container.schedule(0.025, self)

    def on_timer_task(self, event):
        if self._close_requested:
            self._begin_close()
            return
        if self._main_sender is not None and self._main_sender.credit > 0:
            self._pump()
        self._container.schedule(0.025, self)

    def on_connection_opened(self, event):
        _cbs_logger.debug("[cbs] on_connection_opened")
        # Attach the CBS sender + receiver. Both terminus addresses pinned to "$cbs".
        self._cbs_sender = self._container.create_sender(self._conn, "$cbs", name="cbs-sender")
        self._cbs_receiver = self._container.create_receiver(
            self._conn, "$cbs", name="cbs-receiver"
        )
        # Pin the receiver target explicitly (Azure rejects dynamic terminus).
        self._cbs_receiver.target.address = "$cbs"
        self._cbs_receiver.target.dynamic = False

    def on_link_opened(self, event):
        _cbs_logger.debug(f"[cbs] on_link_opened {event.link.name}")
        try:
            link_name = event.link.name
            if link_name == "cbs-sender":
                self._cbs_sender_opened = True
            elif link_name == "cbs-receiver":
                self._cbs_receiver_opened = True
            elif link_name == "main-sender":
                if not self._init_future.done():
                    self._init_future.set_result(True)
                return
            if self._cbs_sender_opened and self._cbs_receiver_opened and self._cbs_request_id is None:
                self._send_put_token()
        except Exception as exc:
            self._fail_init(exc)

    def _send_put_token(self):
        _cbs_logger.debug(
            "[cbs] _send_put_token: acquiring token (type=%s)",
            self._token_provider.token_type,
        )
        try:
            token_body, expires_on = self._token_provider.acquire()
        except Exception as exc:
            self._fail_init(exc)
            return
        _cbs_logger.debug(f"[cbs] _send_put_token: token len={len(token_body)} exp={expires_on}")
        resource_uri = f"sb://{self._host}/{self._address}"
        self._cbs_request_id = str(uuid.uuid4())
        msg = Message(body=token_body)
        msg.address = "$cbs"
        msg.reply_to = "$cbs"
        msg.id = self._cbs_request_id
        msg.properties = {
            "operation": "put-token",
            "type": self._token_provider.token_type,
            "name": resource_uri,
            "expiration": int(expires_on),
        }
        try:
            self._cbs_sender.send(msg)
            _cbs_logger.debug("[cbs] _send_put_token: sent")
        except Exception as exc:
            _cbs_logger.debug(f"[cbs] _send_put_token: send raised {exc!r}")
            self._fail_init(RuntimeError(f"CBS put-token send failed: {exc}"))

    def on_message(self, event):
        _cbs_logger.debug(f"[cbs] on_message link={event.link.name}")
        # Only CBS replies are expected on this handler's receiver.
        if event.link.name != "cbs-receiver":
            return
        reply = event.message
        _cbs_logger.debug(f"[cbs] on_message correlation_id={reply.correlation_id!r} expected={self._cbs_request_id!r} props={dict(reply.properties or {})}")
        try:
            event.delivery.update(event.delivery.ACCEPTED)
            event.delivery.settle()
        except Exception:
            pass
        # Correlate: only accept the reply matching our put-token request id.
        # Compare as strings to tolerate UUID/bytes/str shapes.
        if str(reply.correlation_id) != str(self._cbs_request_id):
            _cbs_logger.debug("[cbs] on_message: correlation mismatch, ignoring")
            return
        props = reply.properties or {}
        status_code = props.get("status-code") or props.get(symbol("status-code")) or 0
        status_desc = props.get("status-description") or props.get(symbol("status-description")) or ""
        _cbs_logger.debug(f"[cbs] on_message: status_code={status_code} desc={status_desc!r}")
        if status_code in (200, 202):
            try:
                self._main_sender = self._container.create_sender(
                    self._conn, self._address, name="main-sender", options=AtLeastOnce()
                )
                _cbs_logger.debug("[cbs] on_message: main-sender create requested")
            except Exception as exc:
                _cbs_logger.debug(f"[cbs] on_message: create_sender raised {exc!r}")
                self._fail_init(exc)
        else:
            self._fail_init(RuntimeError(
                f"CBS put-token rejected: status_code={status_code} {status_desc!r}"
            ))

    # ---- outbound sends ----

    def on_sendable(self, event):
        if event.link is self._main_sender:
            self._pump()

    def _pump(self):
        if self._main_sender is None or self._failed:
            return
        while self._main_sender.credit > 0:
            try:
                req = self._send_queue.get_nowait()
            except queue.Empty:
                return
            if req is None:  # close sentinel
                self._begin_close()
                return
            msg, fut = req
            tag = str(uuid.uuid4()).encode()
            try:
                delivery = self._main_sender.send(msg, tag=tag)
            except Exception as exc:
                if not fut.done():
                    fut.set_exception(exc)
                continue
            self._pending[tag] = fut
            # delivery.tag is what comes back on disposition events
            self._pending[delivery.tag] = fut

    def on_accepted(self, event):
        fut = self._pending.pop(event.delivery.tag, None)
        event.delivery.settle()
        if fut is not None and not fut.done():
            fut.set_result(True)

    def on_rejected(self, event):
        self._fail_delivery(event, "rejected")

    def on_released(self, event):
        self._fail_delivery(event, "released")

    def on_modified(self, event):
        self._fail_delivery(event, "modified")

    def _fail_delivery(self, event, reason):
        fut = self._pending.pop(event.delivery.tag, None)
        event.delivery.settle()
        if fut is not None and not fut.done():
            fut.set_exception(RuntimeError(f"Send failed: {reason}"))

    # ---- error / close ----

    def on_inject_close(self, event):
        self._begin_close()

    def request_close(self):
        """Called from the producer thread; reactor picks it up on next timer tick."""
        self._close_requested = True

    def _begin_close(self):
        try:
            if self._main_sender:
                self._main_sender.close()
        except Exception:
            pass
        try:
            if self._cbs_sender:
                self._cbs_sender.close()
            if self._cbs_receiver:
                self._cbs_receiver.close()
        except Exception:
            pass
        try:
            if self._conn:
                self._conn.close()
        except Exception:
            pass

    def on_transport_error(self, event):
        self._fail_all(RuntimeError(f"Transport error: {event.transport.condition}"))

    def on_connection_error(self, event):
        cond = event.connection.remote_condition
        self._fail_all(RuntimeError(f"Connection error: {cond}"))

    def on_link_error(self, event):
        cond = event.link.remote_condition
        self._fail_all(RuntimeError(f"Link error on {event.link.name}: {cond}"))

    def on_disconnected(self, event):
        _cbs_logger.debug("[cbs] on_disconnected")
        self._fail_all(RuntimeError("Disconnected"))
        self._close_event.set()

    def _fail_init(self, exc):
        _cbs_logger.debug(f"[cbs] _fail_init: {exc!r}")
        self._failed = True
        if not self._init_future.done():
            self._init_future.set_exception(exc)

    def _fail_all(self, exc):
        self._failed = True
        if not self._init_future.done():
            self._init_future.set_exception(exc)
        # Drain queue
        while True:
            try:
                req = self._send_queue.get_nowait()
            except queue.Empty:
                break
            if req is None:
                continue
            _, fut = req
            if not fut.done():
                fut.set_exception(exc)
        for fut in list(self._pending.values()):
            if not fut.done():
                fut.set_exception(exc)
        self._pending.clear()
from usgs_iv_amqp_producer_data import Site
from usgs_iv_amqp_producer_data import SiteTimeseries
from usgs_iv_amqp_producer_data import OtherParameter
from usgs_iv_amqp_producer_data import Precipitation
from usgs_iv_amqp_producer_data import Streamflow
from usgs_iv_amqp_producer_data import GageHeight
from usgs_iv_amqp_producer_data import WaterTemperature
from usgs_iv_amqp_producer_data import DissolvedOxygen
from usgs_iv_amqp_producer_data import PH
from usgs_iv_amqp_producer_data import SpecificConductance
from usgs_iv_amqp_producer_data import Turbidity
from usgs_iv_amqp_producer_data import AirTemperature
from usgs_iv_amqp_producer_data import WindSpeed
from usgs_iv_amqp_producer_data import WindDirection
from usgs_iv_amqp_producer_data import RelativeHumidity
from usgs_iv_amqp_producer_data import BarometricPressure
from usgs_iv_amqp_producer_data import TurbidityFNU
from usgs_iv_amqp_producer_data import FDOM
from usgs_iv_amqp_producer_data import ReservoirStorage
from usgs_iv_amqp_producer_data import LakeElevationNGVD29
from usgs_iv_amqp_producer_data import WaterDepth
from usgs_iv_amqp_producer_data import EquipmentStatus
from usgs_iv_amqp_producer_data import TidallyFilteredDischarge
from usgs_iv_amqp_producer_data import WaterVelocity
from usgs_iv_amqp_producer_data import EstuaryElevationNGVD29
from usgs_iv_amqp_producer_data import LakeElevationNAVD88
from usgs_iv_amqp_producer_data import Salinity
from usgs_iv_amqp_producer_data import GateOpening

class USGSSitesAmqpProducer:
    """
    Producer class to send messages in the `USGS.Sites.amqp` message group via AMQP 1.0 protocol.
    """
    
    def __init__(self, 
                 host: str,
                 address: str,
                 port: int = 5672,
                 username: typing.Optional[str] = None,
                 password: typing.Optional[str] = None,
                 content_mode: typing.Literal['structured', 'binary'] = 'structured',
                 format_type: str = 'application/json',
                 credential: typing.Optional["TokenCredential"] = None,
                 entra_audience: str = "https://servicebus.azure.net/.default",
                 sas_key_name: typing.Optional[str] = None,
                 sas_key: typing.Optional[str] = None,
                 sas_token_ttl_seconds: int = 3600,
                 use_tls: bool = True,
                 ):
        """
        Initialize the AMQP producer
        
        Args:
            host (str): The AMQP broker hostname
            address (str): The AMQP address (queue or topic)
            port (int): The AMQP broker port (default: 5672)
            username (typing.Optional[str]): Optional username for SASL PLAIN authentication
            password (typing.Optional[str]): Optional password for SASL PLAIN authentication
            content_mode (typing.Literal['structured', 'binary']): CloudEvents content mode (default: 'structured')
            format_type (str): Content type format for structured mode (default: 'application/json')
            credential (typing.Optional[TokenCredential]): An azure-identity TokenCredential
                (e.g. DefaultAzureCredential). When provided, SASL ANONYMOUS is used and an
                Entra ID JWT is presented via AMQP CBS put-token (``type=jwt``). Mutually
                exclusive with username/password and with sas_key_name/sas_key.
            entra_audience (str): AAD scope used to acquire the JWT
                (default: 'https://servicebus.azure.net/.default' -- targets Azure servicebus).
                Override only when targeting a non-standard cloud or cross-targeting (e.g.
                an Event Hubs client talking to a Service Bus entity, or vice-versa).
            sas_key_name (typing.Optional[str]): SAS policy/key name (e.g.
                ``RootManageSharedAccessKey``). When set with ``sas_key``, SASL ANONYMOUS
                is used and a SAS token is presented via AMQP CBS put-token
                (``type=servicebus.windows.net:sastoken``). Required for the Service Bus
                emulator and for namespaces configured for SAS authentication.
                Mutually exclusive with credential and with username/password.
            sas_key (typing.Optional[str]): SAS key value (base64) used to sign the token.
            sas_token_ttl_seconds (int): Lifetime of each minted SAS token (default: 3600).
            use_tls (bool): If True (default), connect via amqps:// on port 5671 unless port
                is explicitly set. Required for Azure servicebus; set to False
                for the local Service Bus emulator (plain AMQP on 5672).
        """
        self.host = host
        self.port = port
        self.address = address
        self.username = username
        self.password = password
        self.content_mode = content_mode
        self.format_type = format_type
        self._credential = credential
        self._entra_audience = entra_audience
        self._sas_key_name = sas_key_name
        self._sas_key = sas_key
        self._sas_token_ttl = int(sas_token_ttl_seconds)
        self._use_tls = use_tls

        _sas_configured = bool(sas_key_name or sas_key)
        if _sas_configured and not (sas_key_name and sas_key):
            raise ValueError(
                "sas_key_name and sas_key must both be provided for SAS CBS auth."
            )
        if self._credential is not None and _sas_configured:
            raise ValueError(
                "credential is mutually exclusive with sas_key_name/sas_key. "
                "Choose Entra ID OR SAS for CBS authentication."
            )
        if (self._credential is not None or _sas_configured) and (self.username or self.password):
            raise ValueError(
                "CBS auth (credential or SAS) is mutually exclusive with "
                "username/password SASL PLAIN."
            )
        self._cbs_enabled = self._credential is not None or _sas_configured
        if self._credential is not None and port == 5672:
            # Default to AMQPS for Entra path; caller can override explicitly.
            self.port = 5671
        if self._cbs_enabled:
            self._init_reactor()
        else:
            connection_url = self._build_connection_url()
            self._connection = BlockingConnection(connection_url, timeout=30)
            self._sender = self._connection.create_sender(self.address)

    def _init_reactor(self):
        """Start the proton reactor thread and block until CBS handshake completes.

        On failure, the exception is propagated out of ``__init__`` so callers
        get a clean error rather than discovering the problem on first send.
        """
        if self._credential is not None:
            token_provider: _CbsTokenProvider = _JwtTokenProvider(
                self._credential, self._entra_audience
            )
        else:
            resource_uri = f"sb://{self.host}/{self.address}"
            token_provider = _SasTokenProvider(
                self._sas_key_name, self._sas_key, resource_uri,
                ttl_seconds=self._sas_token_ttl,
            )

        self._send_queue: "queue.Queue" = queue.Queue()
        self._init_future: "concurrent.futures.Future" = concurrent.futures.Future()
        self._close_event = threading.Event()
        self._handler = _CbsAzureHandler(
            host=self.host,
            port=self.port,
            address=self.address,
            token_provider=token_provider,
            use_tls=self._use_tls,
            init_future=self._init_future,
            send_queue=self._send_queue,
            close_event=self._close_event,
        )

        def _run():
            import traceback as _tb
            try:
                Container(self._handler).run()
            except Exception as exc:
                _cbs_logger.debug(f"[cbs] reactor crashed: {exc!r}\n{_tb.format_exc()}")
                if not self._init_future.done():
                    self._init_future.set_exception(exc)
            finally:
                self._close_event.set()

        self._reactor_thread = threading.Thread(
            target=_run, name="amqp-cbs-reactor", daemon=True
        )
        self._reactor_thread.start()

        try:
            self._init_future.result(timeout=60)
        except Exception:
            try:
                self._handler.request_close()
            except Exception:
                pass
            self._close_event.wait(timeout=10)
            raise

    def _send_via_reactor(self, amqp_msg: Message, timeout: float = 30.0) -> None:
        fut: "concurrent.futures.Future" = concurrent.futures.Future()
        self._send_queue.put((amqp_msg, fut))
        fut.result(timeout=timeout)
    
    def _build_connection_url(self) -> str:
        if self.username and self.password:
            user = quote_plus(self.username)
            pwd = quote_plus(self.password)
            return f"amqp://{user}:{pwd}@{self.host}:{self.port}"
        return f"amqp://{self.host}:{self.port}"

    def _serialize_payload(self, data: typing.Any, content_type: str) -> bytes:
        if data is None:
            return b''
        if hasattr(data, 'to_byte_array'):
            payload = data.to_byte_array(content_type)
        elif hasattr(data, 'to_dict'):
            payload = json.dumps(data.to_dict())
        elif isinstance(data, (bytes, bytearray)):
            payload = bytes(data)
        else:
            payload = json.dumps(data)
        # to_byte_array may return str for text content types (e.g. JSON);
        # we always emit bytes so the AMQP body is a binary section rather
        # than an AMQP string section containing escaped JSON.
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        return payload

    @staticmethod
    def _ce_headers_to_amqp_properties(headers: typing.Mapping[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        """Translate cloudevents-sdk HTTP-style headers (``ce-foo``) into the
        CloudEvents AMQP 1.0 Protocol Binding (v1.0.2 §3.1) form
        (``cloudEvents:foo``). ``content-type`` is carried separately on the
        AMQP properties section and is therefore dropped here.
        """
        out: typing.Dict[str, typing.Any] = {}
        for k, v in (headers or {}).items():
            if v is None:
                continue
            lk = str(k)
            low = lk.lower()
            if low.startswith('ce-'):
                out['cloudEvents:' + lk[3:]] = v
            elif low == 'content-type':
                continue
            else:
                out[lk] = v
        return out

    
    
    def send_site(self,
        data: Site,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.Sites.amqp.Site` message
        A reference record for one United States streamgages and other monitoring site published by the U.S. Geological Survey (USGS) Water Services API. It fires when the bridge publishes or refreshes the station catalog so consumers can interpret measurement events.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            data (Site): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.Sites.Site",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}".format(agency_cd=_agency_cd, site_no=_site_no),
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}".format(agency_cd=_agency_cd, site_no=_site_no)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_site_batch(self,
        data_array: typing.List[Site],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.Sites.amqp.Site` messages
        
        Args:
            data_array (typing.List[Site]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_site(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                content_type=content_type)
    
    
    def close(self) -> None:
        """
        Close the producer and clean up resources
        """
        if getattr(self, "_handler", None) is not None:
            try:
                self._handler.request_close()
            except Exception:  # pragma: no cover - best-effort cleanup
                pass
            self._close_event.wait(timeout=10)
            self._handler = None
            return
        if hasattr(self, '_sender') and self._sender:
            try:
                self._sender.close()
            except Exception:  # pragma: no cover - best-effort cleanup
                pass
            finally:
                self._sender = None
        if hasattr(self, '_connection') and self._connection:
            try:
                self._connection.close()
            except Exception:  # pragma: no cover - best-effort cleanup
                pass
            finally:
                self._connection = None



class USGSSiteTimeseriesAmqpProducer:
    """
    Producer class to send messages in the `USGS.SiteTimeseries.amqp` message group via AMQP 1.0 protocol.
    """
    
    def __init__(self, 
                 host: str,
                 address: str,
                 port: int = 5672,
                 username: typing.Optional[str] = None,
                 password: typing.Optional[str] = None,
                 content_mode: typing.Literal['structured', 'binary'] = 'structured',
                 format_type: str = 'application/json',
                 credential: typing.Optional["TokenCredential"] = None,
                 entra_audience: str = "https://servicebus.azure.net/.default",
                 sas_key_name: typing.Optional[str] = None,
                 sas_key: typing.Optional[str] = None,
                 sas_token_ttl_seconds: int = 3600,
                 use_tls: bool = True,
                 ):
        """
        Initialize the AMQP producer
        
        Args:
            host (str): The AMQP broker hostname
            address (str): The AMQP address (queue or topic)
            port (int): The AMQP broker port (default: 5672)
            username (typing.Optional[str]): Optional username for SASL PLAIN authentication
            password (typing.Optional[str]): Optional password for SASL PLAIN authentication
            content_mode (typing.Literal['structured', 'binary']): CloudEvents content mode (default: 'structured')
            format_type (str): Content type format for structured mode (default: 'application/json')
            credential (typing.Optional[TokenCredential]): An azure-identity TokenCredential
                (e.g. DefaultAzureCredential). When provided, SASL ANONYMOUS is used and an
                Entra ID JWT is presented via AMQP CBS put-token (``type=jwt``). Mutually
                exclusive with username/password and with sas_key_name/sas_key.
            entra_audience (str): AAD scope used to acquire the JWT
                (default: 'https://servicebus.azure.net/.default' -- targets Azure servicebus).
                Override only when targeting a non-standard cloud or cross-targeting (e.g.
                an Event Hubs client talking to a Service Bus entity, or vice-versa).
            sas_key_name (typing.Optional[str]): SAS policy/key name (e.g.
                ``RootManageSharedAccessKey``). When set with ``sas_key``, SASL ANONYMOUS
                is used and a SAS token is presented via AMQP CBS put-token
                (``type=servicebus.windows.net:sastoken``). Required for the Service Bus
                emulator and for namespaces configured for SAS authentication.
                Mutually exclusive with credential and with username/password.
            sas_key (typing.Optional[str]): SAS key value (base64) used to sign the token.
            sas_token_ttl_seconds (int): Lifetime of each minted SAS token (default: 3600).
            use_tls (bool): If True (default), connect via amqps:// on port 5671 unless port
                is explicitly set. Required for Azure servicebus; set to False
                for the local Service Bus emulator (plain AMQP on 5672).
        """
        self.host = host
        self.port = port
        self.address = address
        self.username = username
        self.password = password
        self.content_mode = content_mode
        self.format_type = format_type
        self._credential = credential
        self._entra_audience = entra_audience
        self._sas_key_name = sas_key_name
        self._sas_key = sas_key
        self._sas_token_ttl = int(sas_token_ttl_seconds)
        self._use_tls = use_tls

        _sas_configured = bool(sas_key_name or sas_key)
        if _sas_configured and not (sas_key_name and sas_key):
            raise ValueError(
                "sas_key_name and sas_key must both be provided for SAS CBS auth."
            )
        if self._credential is not None and _sas_configured:
            raise ValueError(
                "credential is mutually exclusive with sas_key_name/sas_key. "
                "Choose Entra ID OR SAS for CBS authentication."
            )
        if (self._credential is not None or _sas_configured) and (self.username or self.password):
            raise ValueError(
                "CBS auth (credential or SAS) is mutually exclusive with "
                "username/password SASL PLAIN."
            )
        self._cbs_enabled = self._credential is not None or _sas_configured
        if self._credential is not None and port == 5672:
            # Default to AMQPS for Entra path; caller can override explicitly.
            self.port = 5671
        if self._cbs_enabled:
            self._init_reactor()
        else:
            connection_url = self._build_connection_url()
            self._connection = BlockingConnection(connection_url, timeout=30)
            self._sender = self._connection.create_sender(self.address)

    def _init_reactor(self):
        """Start the proton reactor thread and block until CBS handshake completes.

        On failure, the exception is propagated out of ``__init__`` so callers
        get a clean error rather than discovering the problem on first send.
        """
        if self._credential is not None:
            token_provider: _CbsTokenProvider = _JwtTokenProvider(
                self._credential, self._entra_audience
            )
        else:
            resource_uri = f"sb://{self.host}/{self.address}"
            token_provider = _SasTokenProvider(
                self._sas_key_name, self._sas_key, resource_uri,
                ttl_seconds=self._sas_token_ttl,
            )

        self._send_queue: "queue.Queue" = queue.Queue()
        self._init_future: "concurrent.futures.Future" = concurrent.futures.Future()
        self._close_event = threading.Event()
        self._handler = _CbsAzureHandler(
            host=self.host,
            port=self.port,
            address=self.address,
            token_provider=token_provider,
            use_tls=self._use_tls,
            init_future=self._init_future,
            send_queue=self._send_queue,
            close_event=self._close_event,
        )

        def _run():
            import traceback as _tb
            try:
                Container(self._handler).run()
            except Exception as exc:
                _cbs_logger.debug(f"[cbs] reactor crashed: {exc!r}\n{_tb.format_exc()}")
                if not self._init_future.done():
                    self._init_future.set_exception(exc)
            finally:
                self._close_event.set()

        self._reactor_thread = threading.Thread(
            target=_run, name="amqp-cbs-reactor", daemon=True
        )
        self._reactor_thread.start()

        try:
            self._init_future.result(timeout=60)
        except Exception:
            try:
                self._handler.request_close()
            except Exception:
                pass
            self._close_event.wait(timeout=10)
            raise

    def _send_via_reactor(self, amqp_msg: Message, timeout: float = 30.0) -> None:
        fut: "concurrent.futures.Future" = concurrent.futures.Future()
        self._send_queue.put((amqp_msg, fut))
        fut.result(timeout=timeout)
    
    def _build_connection_url(self) -> str:
        if self.username and self.password:
            user = quote_plus(self.username)
            pwd = quote_plus(self.password)
            return f"amqp://{user}:{pwd}@{self.host}:{self.port}"
        return f"amqp://{self.host}:{self.port}"

    def _serialize_payload(self, data: typing.Any, content_type: str) -> bytes:
        if data is None:
            return b''
        if hasattr(data, 'to_byte_array'):
            payload = data.to_byte_array(content_type)
        elif hasattr(data, 'to_dict'):
            payload = json.dumps(data.to_dict())
        elif isinstance(data, (bytes, bytearray)):
            payload = bytes(data)
        else:
            payload = json.dumps(data)
        # to_byte_array may return str for text content types (e.g. JSON);
        # we always emit bytes so the AMQP body is a binary section rather
        # than an AMQP string section containing escaped JSON.
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        return payload

    @staticmethod
    def _ce_headers_to_amqp_properties(headers: typing.Mapping[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        """Translate cloudevents-sdk HTTP-style headers (``ce-foo``) into the
        CloudEvents AMQP 1.0 Protocol Binding (v1.0.2 §3.1) form
        (``cloudEvents:foo``). ``content-type`` is carried separately on the
        AMQP properties section and is therefore dropped here.
        """
        out: typing.Dict[str, typing.Any] = {}
        for k, v in (headers or {}).items():
            if v is None:
                continue
            lk = str(k)
            low = lk.lower()
            if low.startswith('ce-'):
                out['cloudEvents:' + lk[3:]] = v
            elif low == 'content-type':
                continue
            else:
                out[lk] = v
        return out

    
    
    def send_site_timeseries(self,
        data: SiteTimeseries,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.SiteTimeseries.amqp.SiteTimeseries` message
        A reference record for one United States streamgages and other monitoring site published by the U.S. Geological Survey (USGS) Water Services API. It fires when the bridge publishes or refreshes the station catalog so consumers can interpret measurement events.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            data (SiteTimeseries): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.Sites.SiteTimeseries",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_site_timeseries_batch(self,
        data_array: typing.List[SiteTimeseries],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.SiteTimeseries.amqp.SiteTimeseries` messages
        
        Args:
            data_array (typing.List[SiteTimeseries]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_site_timeseries(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                content_type=content_type)
    
    
    def close(self) -> None:
        """
        Close the producer and clean up resources
        """
        if getattr(self, "_handler", None) is not None:
            try:
                self._handler.request_close()
            except Exception:  # pragma: no cover - best-effort cleanup
                pass
            self._close_event.wait(timeout=10)
            self._handler = None
            return
        if hasattr(self, '_sender') and self._sender:
            try:
                self._sender.close()
            except Exception:  # pragma: no cover - best-effort cleanup
                pass
            finally:
                self._sender = None
        if hasattr(self, '_connection') and self._connection:
            try:
                self._connection.close()
            except Exception:  # pragma: no cover - best-effort cleanup
                pass
            finally:
                self._connection = None



class USGSInstantaneousValuesAmqpProducer:
    """
    Producer class to send messages in the `USGS.InstantaneousValues.amqp` message group via AMQP 1.0 protocol.
    """
    
    def __init__(self, 
                 host: str,
                 address: str,
                 port: int = 5672,
                 username: typing.Optional[str] = None,
                 password: typing.Optional[str] = None,
                 content_mode: typing.Literal['structured', 'binary'] = 'structured',
                 format_type: str = 'application/json',
                 credential: typing.Optional["TokenCredential"] = None,
                 entra_audience: str = "https://servicebus.azure.net/.default",
                 sas_key_name: typing.Optional[str] = None,
                 sas_key: typing.Optional[str] = None,
                 sas_token_ttl_seconds: int = 3600,
                 use_tls: bool = True,
                 ):
        """
        Initialize the AMQP producer
        
        Args:
            host (str): The AMQP broker hostname
            address (str): The AMQP address (queue or topic)
            port (int): The AMQP broker port (default: 5672)
            username (typing.Optional[str]): Optional username for SASL PLAIN authentication
            password (typing.Optional[str]): Optional password for SASL PLAIN authentication
            content_mode (typing.Literal['structured', 'binary']): CloudEvents content mode (default: 'structured')
            format_type (str): Content type format for structured mode (default: 'application/json')
            credential (typing.Optional[TokenCredential]): An azure-identity TokenCredential
                (e.g. DefaultAzureCredential). When provided, SASL ANONYMOUS is used and an
                Entra ID JWT is presented via AMQP CBS put-token (``type=jwt``). Mutually
                exclusive with username/password and with sas_key_name/sas_key.
            entra_audience (str): AAD scope used to acquire the JWT
                (default: 'https://servicebus.azure.net/.default' -- targets Azure servicebus).
                Override only when targeting a non-standard cloud or cross-targeting (e.g.
                an Event Hubs client talking to a Service Bus entity, or vice-versa).
            sas_key_name (typing.Optional[str]): SAS policy/key name (e.g.
                ``RootManageSharedAccessKey``). When set with ``sas_key``, SASL ANONYMOUS
                is used and a SAS token is presented via AMQP CBS put-token
                (``type=servicebus.windows.net:sastoken``). Required for the Service Bus
                emulator and for namespaces configured for SAS authentication.
                Mutually exclusive with credential and with username/password.
            sas_key (typing.Optional[str]): SAS key value (base64) used to sign the token.
            sas_token_ttl_seconds (int): Lifetime of each minted SAS token (default: 3600).
            use_tls (bool): If True (default), connect via amqps:// on port 5671 unless port
                is explicitly set. Required for Azure servicebus; set to False
                for the local Service Bus emulator (plain AMQP on 5672).
        """
        self.host = host
        self.port = port
        self.address = address
        self.username = username
        self.password = password
        self.content_mode = content_mode
        self.format_type = format_type
        self._credential = credential
        self._entra_audience = entra_audience
        self._sas_key_name = sas_key_name
        self._sas_key = sas_key
        self._sas_token_ttl = int(sas_token_ttl_seconds)
        self._use_tls = use_tls

        _sas_configured = bool(sas_key_name or sas_key)
        if _sas_configured and not (sas_key_name and sas_key):
            raise ValueError(
                "sas_key_name and sas_key must both be provided for SAS CBS auth."
            )
        if self._credential is not None and _sas_configured:
            raise ValueError(
                "credential is mutually exclusive with sas_key_name/sas_key. "
                "Choose Entra ID OR SAS for CBS authentication."
            )
        if (self._credential is not None or _sas_configured) and (self.username or self.password):
            raise ValueError(
                "CBS auth (credential or SAS) is mutually exclusive with "
                "username/password SASL PLAIN."
            )
        self._cbs_enabled = self._credential is not None or _sas_configured
        if self._credential is not None and port == 5672:
            # Default to AMQPS for Entra path; caller can override explicitly.
            self.port = 5671
        if self._cbs_enabled:
            self._init_reactor()
        else:
            connection_url = self._build_connection_url()
            self._connection = BlockingConnection(connection_url, timeout=30)
            self._sender = self._connection.create_sender(self.address)

    def _init_reactor(self):
        """Start the proton reactor thread and block until CBS handshake completes.

        On failure, the exception is propagated out of ``__init__`` so callers
        get a clean error rather than discovering the problem on first send.
        """
        if self._credential is not None:
            token_provider: _CbsTokenProvider = _JwtTokenProvider(
                self._credential, self._entra_audience
            )
        else:
            resource_uri = f"sb://{self.host}/{self.address}"
            token_provider = _SasTokenProvider(
                self._sas_key_name, self._sas_key, resource_uri,
                ttl_seconds=self._sas_token_ttl,
            )

        self._send_queue: "queue.Queue" = queue.Queue()
        self._init_future: "concurrent.futures.Future" = concurrent.futures.Future()
        self._close_event = threading.Event()
        self._handler = _CbsAzureHandler(
            host=self.host,
            port=self.port,
            address=self.address,
            token_provider=token_provider,
            use_tls=self._use_tls,
            init_future=self._init_future,
            send_queue=self._send_queue,
            close_event=self._close_event,
        )

        def _run():
            import traceback as _tb
            try:
                Container(self._handler).run()
            except Exception as exc:
                _cbs_logger.debug(f"[cbs] reactor crashed: {exc!r}\n{_tb.format_exc()}")
                if not self._init_future.done():
                    self._init_future.set_exception(exc)
            finally:
                self._close_event.set()

        self._reactor_thread = threading.Thread(
            target=_run, name="amqp-cbs-reactor", daemon=True
        )
        self._reactor_thread.start()

        try:
            self._init_future.result(timeout=60)
        except Exception:
            try:
                self._handler.request_close()
            except Exception:
                pass
            self._close_event.wait(timeout=10)
            raise

    def _send_via_reactor(self, amqp_msg: Message, timeout: float = 30.0) -> None:
        fut: "concurrent.futures.Future" = concurrent.futures.Future()
        self._send_queue.put((amqp_msg, fut))
        fut.result(timeout=timeout)
    
    def _build_connection_url(self) -> str:
        if self.username and self.password:
            user = quote_plus(self.username)
            pwd = quote_plus(self.password)
            return f"amqp://{user}:{pwd}@{self.host}:{self.port}"
        return f"amqp://{self.host}:{self.port}"

    def _serialize_payload(self, data: typing.Any, content_type: str) -> bytes:
        if data is None:
            return b''
        if hasattr(data, 'to_byte_array'):
            payload = data.to_byte_array(content_type)
        elif hasattr(data, 'to_dict'):
            payload = json.dumps(data.to_dict())
        elif isinstance(data, (bytes, bytearray)):
            payload = bytes(data)
        else:
            payload = json.dumps(data)
        # to_byte_array may return str for text content types (e.g. JSON);
        # we always emit bytes so the AMQP body is a binary section rather
        # than an AMQP string section containing escaped JSON.
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        return payload

    @staticmethod
    def _ce_headers_to_amqp_properties(headers: typing.Mapping[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        """Translate cloudevents-sdk HTTP-style headers (``ce-foo``) into the
        CloudEvents AMQP 1.0 Protocol Binding (v1.0.2 §3.1) form
        (``cloudEvents:foo``). ``content-type`` is carried separately on the
        AMQP properties section and is therefore dropped here.
        """
        out: typing.Dict[str, typing.Any] = {}
        for k, v in (headers or {}).items():
            if v is None:
                continue
            lk = str(k)
            low = lk.lower()
            if low.startswith('ce-'):
                out['cloudEvents:' + lk[3:]] = v
            elif low == 'content-type':
                continue
            else:
                out[lk] = v
        return out

    
    
    def send_other_parameter(self,
        data: OtherParameter,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.OtherParameter` message
        A other parameter event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (OtherParameter): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.OtherParameter",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_other_parameter_batch(self,
        data_array: typing.List[OtherParameter],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.OtherParameter` messages
        
        Args:
            data_array (typing.List[OtherParameter]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_other_parameter(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_precipitation(self,
        data: Precipitation,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.Precipitation` message
        A precipitation event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (Precipitation): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.Precipitation",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_precipitation_batch(self,
        data_array: typing.List[Precipitation],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.Precipitation` messages
        
        Args:
            data_array (typing.List[Precipitation]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_precipitation(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_streamflow(self,
        data: Streamflow,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.Streamflow` message
        A current measurement from the U.S. Geological Survey (USGS) Water Services API for one monitoring site. It carries instantaneous water observations such as gauge height, discharge, and temperature when the upstream feed reports a new or refreshed value.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (Streamflow): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.Streamflow",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_streamflow_batch(self,
        data_array: typing.List[Streamflow],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.Streamflow` messages
        
        Args:
            data_array (typing.List[Streamflow]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_streamflow(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_gage_height(self,
        data: GageHeight,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.GageHeight` message
        A gage height event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (GageHeight): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.GageHeight",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_gage_height_batch(self,
        data_array: typing.List[GageHeight],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.GageHeight` messages
        
        Args:
            data_array (typing.List[GageHeight]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_gage_height(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_water_temperature(self,
        data: WaterTemperature,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.WaterTemperature` message
        A current measurement from the U.S. Geological Survey (USGS) Water Services API for one monitoring site. It carries instantaneous water observations such as gauge height, discharge, and temperature when the upstream feed reports a new or refreshed value.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (WaterTemperature): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.WaterTemperature",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_water_temperature_batch(self,
        data_array: typing.List[WaterTemperature],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.WaterTemperature` messages
        
        Args:
            data_array (typing.List[WaterTemperature]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_water_temperature(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_dissolved_oxygen(self,
        data: DissolvedOxygen,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.DissolvedOxygen` message
        A dissolved oxygen event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (DissolvedOxygen): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.DissolvedOxygen",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_dissolved_oxygen_batch(self,
        data_array: typing.List[DissolvedOxygen],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.DissolvedOxygen` messages
        
        Args:
            data_array (typing.List[DissolvedOxygen]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_dissolved_oxygen(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_ph(self,
        data: PH,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.pH` message
        A p h event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (PH): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.pH",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_ph_batch(self,
        data_array: typing.List[PH],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.pH` messages
        
        Args:
            data_array (typing.List[PH]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_ph(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_specific_conductance(self,
        data: SpecificConductance,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.SpecificConductance` message
        A specific conductance event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (SpecificConductance): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.SpecificConductance",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_specific_conductance_batch(self,
        data_array: typing.List[SpecificConductance],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.SpecificConductance` messages
        
        Args:
            data_array (typing.List[SpecificConductance]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_specific_conductance(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_turbidity(self,
        data: Turbidity,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.Turbidity` message
        A turbidity event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (Turbidity): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.Turbidity",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_turbidity_batch(self,
        data_array: typing.List[Turbidity],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.Turbidity` messages
        
        Args:
            data_array (typing.List[Turbidity]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_turbidity(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_air_temperature(self,
        data: AirTemperature,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.AirTemperature` message
        A air temperature event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (AirTemperature): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.AirTemperature",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_air_temperature_batch(self,
        data_array: typing.List[AirTemperature],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.AirTemperature` messages
        
        Args:
            data_array (typing.List[AirTemperature]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_air_temperature(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_wind_speed(self,
        data: WindSpeed,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.WindSpeed` message
        A wind speed event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (WindSpeed): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.WindSpeed",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_wind_speed_batch(self,
        data_array: typing.List[WindSpeed],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.WindSpeed` messages
        
        Args:
            data_array (typing.List[WindSpeed]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_wind_speed(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_wind_direction(self,
        data: WindDirection,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.WindDirection` message
        A wind direction event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (WindDirection): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.WindDirection",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_wind_direction_batch(self,
        data_array: typing.List[WindDirection],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.WindDirection` messages
        
        Args:
            data_array (typing.List[WindDirection]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_wind_direction(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_relative_humidity(self,
        data: RelativeHumidity,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.RelativeHumidity` message
        A relative humidity event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (RelativeHumidity): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.RelativeHumidity",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_relative_humidity_batch(self,
        data_array: typing.List[RelativeHumidity],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.RelativeHumidity` messages
        
        Args:
            data_array (typing.List[RelativeHumidity]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_relative_humidity(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_barometric_pressure(self,
        data: BarometricPressure,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.BarometricPressure` message
        A barometric pressure event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (BarometricPressure): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.BarometricPressure",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_barometric_pressure_batch(self,
        data_array: typing.List[BarometricPressure],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.BarometricPressure` messages
        
        Args:
            data_array (typing.List[BarometricPressure]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_barometric_pressure(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_turbidity_fnu(self,
        data: TurbidityFNU,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.TurbidityFNU` message
        A turbidity f n u event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (TurbidityFNU): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.TurbidityFNU",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_turbidity_fnu_batch(self,
        data_array: typing.List[TurbidityFNU],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.TurbidityFNU` messages
        
        Args:
            data_array (typing.List[TurbidityFNU]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_turbidity_fnu(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_fdom(self,
        data: FDOM,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.fDOM` message
        A f d o m event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (FDOM): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.fDOM",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_fdom_batch(self,
        data_array: typing.List[FDOM],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.fDOM` messages
        
        Args:
            data_array (typing.List[FDOM]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_fdom(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_reservoir_storage(self,
        data: ReservoirStorage,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.ReservoirStorage` message
        A current reservoir record from the U.S. Geological Survey (USGS) Water Services API. It reports the latest storage, elevation, capacity, or related reservoir status available for one reservoir.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (ReservoirStorage): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.ReservoirStorage",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_reservoir_storage_batch(self,
        data_array: typing.List[ReservoirStorage],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.ReservoirStorage` messages
        
        Args:
            data_array (typing.List[ReservoirStorage]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_reservoir_storage(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_lake_elevation_ngvd29(self,
        data: LakeElevationNGVD29,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.LakeElevationNGVD29` message
        A lake elevation n g v d29 event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (LakeElevationNGVD29): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.LakeElevationNGVD29",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_lake_elevation_ngvd29_batch(self,
        data_array: typing.List[LakeElevationNGVD29],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.LakeElevationNGVD29` messages
        
        Args:
            data_array (typing.List[LakeElevationNGVD29]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_lake_elevation_ngvd29(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_water_depth(self,
        data: WaterDepth,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.WaterDepth` message
        A current measurement from the U.S. Geological Survey (USGS) Water Services API for one monitoring site. It carries instantaneous water observations such as gauge height, discharge, and temperature when the upstream feed reports a new or refreshed value.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (WaterDepth): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.WaterDepth",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_water_depth_batch(self,
        data_array: typing.List[WaterDepth],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.WaterDepth` messages
        
        Args:
            data_array (typing.List[WaterDepth]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_water_depth(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_equipment_status(self,
        data: EquipmentStatus,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.EquipmentStatus` message
        A equipment status event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (EquipmentStatus): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.EquipmentStatus",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_equipment_status_batch(self,
        data_array: typing.List[EquipmentStatus],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.EquipmentStatus` messages
        
        Args:
            data_array (typing.List[EquipmentStatus]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_equipment_status(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_tidally_filtered_discharge(self,
        data: TidallyFilteredDischarge,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.TidallyFilteredDischarge` message
        A tidally filtered discharge event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (TidallyFilteredDischarge): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.TidallyFilteredDischarge",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_tidally_filtered_discharge_batch(self,
        data_array: typing.List[TidallyFilteredDischarge],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.TidallyFilteredDischarge` messages
        
        Args:
            data_array (typing.List[TidallyFilteredDischarge]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_tidally_filtered_discharge(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_water_velocity(self,
        data: WaterVelocity,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.WaterVelocity` message
        A current measurement from the U.S. Geological Survey (USGS) Water Services API for one monitoring site. It carries instantaneous water observations such as gauge height, discharge, and temperature when the upstream feed reports a new or refreshed value.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (WaterVelocity): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.WaterVelocity",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_water_velocity_batch(self,
        data_array: typing.List[WaterVelocity],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.WaterVelocity` messages
        
        Args:
            data_array (typing.List[WaterVelocity]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_water_velocity(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_estuary_elevation_ngvd29(self,
        data: EstuaryElevationNGVD29,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.EstuaryElevationNGVD29` message
        A estuary elevation n g v d29 event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (EstuaryElevationNGVD29): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.EstuaryElevationNGVD29",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_estuary_elevation_ngvd29_batch(self,
        data_array: typing.List[EstuaryElevationNGVD29],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.EstuaryElevationNGVD29` messages
        
        Args:
            data_array (typing.List[EstuaryElevationNGVD29]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_estuary_elevation_ngvd29(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_lake_elevation_navd88(self,
        data: LakeElevationNAVD88,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.LakeElevationNAVD88` message
        A lake elevation n a v d88 event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (LakeElevationNAVD88): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.LakeElevationNAVD88",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_lake_elevation_navd88_batch(self,
        data_array: typing.List[LakeElevationNAVD88],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.LakeElevationNAVD88` messages
        
        Args:
            data_array (typing.List[LakeElevationNAVD88]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_lake_elevation_navd88(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_salinity(self,
        data: Salinity,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.Salinity` message
        A salinity event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (Salinity): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.Salinity",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_salinity_batch(self,
        data_array: typing.List[Salinity],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.Salinity` messages
        
        Args:
            data_array (typing.List[Salinity]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_salinity(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def send_gate_opening(self,
        data: GateOpening,
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send the `USGS.InstantaneousValues.amqp.GateOpening` message
        A gate opening event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.
        
        Args:
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            data (GateOpening): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "USGS.InstantaneousValues.GateOpening",
            "source":
            "{source_uri}".format(source_uri=_source_uri),
            "subject":
            "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd),
            "time":
            None,  # Will be auto-generated
        }
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)
        
        # Send message
        if getattr(self, "_handler", None) is not None:
            self._send_via_reactor(amqp_msg)
        else:
            self._sender.send(amqp_msg)
    
    def send_gate_opening_batch(self,
        data_array: typing.List[GateOpening],
        _source_uri: str,
        _agency_cd: str,
        _site_no: str,
        _parameter_cd: str,
        _timeseries_cd: str,
        _datetime: str,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `USGS.InstantaneousValues.amqp.GateOpening` messages
        
        Args:
            data_array (typing.List[GateOpening]): Array of message data objects
            _source_uri (str): Value for placeholder source_uri in attribute source
            _agency_cd (str): Value for placeholder agency_cd in attribute subject
            _site_no (str): Value for placeholder site_no in attribute subject
            _parameter_cd (str): Value for placeholder parameter_cd in attribute subject
            _timeseries_cd (str): Value for placeholder timeseries_cd in attribute subject
            _datetime (str): Value for placeholder datetime in attribute time
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_gate_opening(
                data=data,
                _source_uri=_source_uri,
                _agency_cd=_agency_cd,
                _site_no=_site_no,
                _parameter_cd=_parameter_cd,
                _timeseries_cd=_timeseries_cd,
                _datetime=_datetime,
                content_type=content_type)
    
    
    def close(self) -> None:
        """
        Close the producer and clean up resources
        """
        if getattr(self, "_handler", None) is not None:
            try:
                self._handler.request_close()
            except Exception:  # pragma: no cover - best-effort cleanup
                pass
            self._close_event.wait(timeout=10)
            self._handler = None
            return
        if hasattr(self, '_sender') and self._sender:
            try:
                self._sender.close()
            except Exception:  # pragma: no cover - best-effort cleanup
                pass
            finally:
                self._sender = None
        if hasattr(self, '_connection') and self._connection:
            try:
                self._connection.close()
            except Exception:  # pragma: no cover - best-effort cleanup
                pass
            finally:
                self._connection = None

