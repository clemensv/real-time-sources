"""PegelOnline → AMQP 1.0 feeder.

Wraps :mod:`pegelonline_core` and the generated AMQP producer to ship
PegelOnline station catalog + current measurements as CloudEvents over
AMQP 1.0. Targets both generic brokers (RabbitMQ AMQP 1.0, ActiveMQ
Artemis, Qpid Dispatch) via SASL PLAIN, and Azure Service Bus / Event
Hubs via Entra ID (CBS put-token, no SAS-key minting).
"""

from .app import main

__all__ = ["main"]
