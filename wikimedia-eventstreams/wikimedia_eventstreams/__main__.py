"""Entry point for python -m wikimedia_eventstreams."""

import sys

from wikimedia_eventstreams.wikimedia_eventstreams import main


if __name__ == "__main__":
    sys.exit(main())
