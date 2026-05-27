#!/bin/bash
set -e

echo "Installing seattle_street_closures_amqp_producer_amqp_producer..."

# Check if poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
fi

# Install dependencies
poetry install

echo "Installation complete!"
echo "Run 'poetry run pytest' to run tests"