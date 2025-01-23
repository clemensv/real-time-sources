#!/bin/bash

# Function to install the service
install_service() {
    # Print parameters and ask for confirmation
    echo "The following parameters will be used for installation:"
    echo "Antenna Latitude: $ANTENNA_LAT"
    echo "Antenna Longitude: $ANTENNA_LON"
    echo "dump1090 Host: $DUMP1090_HOST"
    echo "dump1090 Port: $DUMP1090_PORT"
    echo "Station ID: $STATIONID"
    echo "Content Mode: $CONTENT_MODE"
    echo "Kafka Bootstrap Servers: $KAFKA_BOOTSTRAP_SERVERS"
    echo "Kafka Topic: $KAFKA_TOPIC"
    echo "SASL Username: $SASL_USERNAME"
    echo "SASL Password: $SASL_PASSWORD"
    echo "Connection String: $CONNECTION_STRING"

    read -p "Do you want to proceed with the installation? (yes/no): " confirmation
    if [[ "$confirmation" != "yes" ]]; then
        echo "Installation aborted."
        exit 0
    fi

    script_dir=$(dirname "$(realpath "$0")")

    # Create user if needed
    if ! id -u mode_s_kafka_bridge >/dev/null 2>&1; then
        sudo useradd -r -s /usr/sbin/nologin -m mode_s_kafka_bridge
    fi

    # Ensure home directory exists and set permissions
    home_dir="/home/mode_s_kafka_bridge"
    sudo mkdir -p "$home_dir"
    sudo chown -R mode_s_kafka_bridge:mode_s_kafka_bridge "$home_dir"

    # Create log directory
    log_dir="/var/log/mode_s_kafka_bridge"
    sudo mkdir -p "$log_dir"
    sudo chown -R mode_s_kafka_bridge:mode_s_kafka_bridge "$log_dir"

    # Create virtual environment
    venv_dir="$home_dir/venv"
    sudo -u mode_s_kafka_bridge python3 -m venv "$venv_dir"
    sudo -u mode_s_kafka_bridge "$venv_dir/bin/pip" install --upgrade pip
    sudo cp -r "$script_dir" "$home_dir/mode_s"
    sudo -u mode_s_kafka_bridge "$venv_dir/bin/pip" install "$home_dir/mode_s"
    

    # Write systemd unit
    service_path="/etc/systemd/system/mode_s_kafka_bridge.service"
    service_content=$(
        cat <<EOF
[Unit]
Description=Mode-S Kafka Bridge service
After=network.target

[Service]
User=mode_s_kafka_bridge
WorkingDirectory=$home_dir
ExecStart=$venv_dir/bin/mode_s_kafka_bridge feed
Environment="STATIONID=$STATIONID"
Environment="CONTENT_MODE=$CONTENT_MODE"
Environment="KAFKA_BOOTSTRAP_SERVERS=$KAFKA_BOOTSTRAP_SERVERS"
Environment="KAFKA_TOPIC=$KAFKA_TOPIC"
Environment="SASL_USERNAME=$SASL_USERNAME"
Environment="SASL_PASSWORD=$SASL_PASSWORD"
Environment="CONNECTION_STRING=$CONNECTION_STRING"
Environment="ANTENNA_LAT=$ANTENNA_LAT"
Environment="ANTENNA_LON=$ANTENNA_LON"
Environment="DUMP1090_HOST=$DUMP1090_HOST"
Environment="DUMP1090_PORT=$DUMP1090_PORT"
StandardOutput=append:/var/log/mode_s_kafka_bridge/stdout.log
StandardError=append:/var/log/mode_s_kafka_bridge/stderr.log
Restart=always

[Install]
WantedBy=multi-user.target
EOF
    )
    echo "$service_content" | sudo tee "$service_path" > /dev/null

    # Reload systemd and enable
    sudo systemctl daemon-reload
    sudo systemctl enable mode_s_kafka_bridge.service

    echo "Service installed. Use 'sudo systemctl start mode_s_kafka_bridge' to run."
}

# Function to uninstall the service
uninstall_service() {
    home_dir="/home/mode_s_kafka_bridge"

    # Stop and disable the service
    sudo systemctl stop mode_s_kafka_bridge.service
    sudo systemctl disable mode_s_kafka_bridge.service

    # Remove the systemd service file
    service_path="/etc/systemd/system/mode_s_kafka_bridge.service"
    if [[ -f "$service_path" ]]; then
        sudo rm "$service_path"
    fi

    # Reload systemd
    sudo systemctl daemon-reload

    # Optionally, remove the user and log directory
    if id -u mode_s_kafka_bridge >/dev/null 2>&1; then
        sudo userdel mode_s_kafka_bridge
    fi
    log_dir="/var/log/mode_s_kafka_bridge"
    if [[ -d "$log_dir" ]]; then
        sudo rm -rf "$log_dir"
    fi

    sudo rm -rf "$home_dir"

    echo "Service uninstalled."
}

# Function to update the service
update_service() {
    script_dir=$(dirname "$(realpath "$0")")
    home_dir="/home/mode_s_kafka_bridge"
    venv_dir="$home_dir/venv"

    # Upgrade the package to the latest version
    sudo cp -r "$script_dir" "$home_dir/mode_s"
    sudo -u mode_s_kafka_bridge "$venv_dir/bin/pip" install --upgrade "$home_dir/mode_s"

    # Restart the service
    sudo systemctl restart mode_s_kafka_bridge.service

    echo "Service updated and restarted."
}

# Set defaults

DUMP1090_HOST="localhost"
DUMP1090_PORT=30005

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --connection-string) CONNECTION_STRING="$2"; shift ;;
        --kafka-bootstrap-servers) KAFKA_BOOTSTRAP_SERVERS="$2"; shift ;;
        --kafka-topic) KAFKA_TOPIC="$2"; shift ;;
        --sasl-username) SASL_USERNAME="$2"; shift ;;
        --sasl-password) SASL_PASSWORD="$2"; shift ;;
        --antenna-lat) ANTENNA_LAT="$2"; shift ;;
        --antenna-lon) ANTENNA_LON="$2"; shift ;;
        --dump1090-host) DUMP1090_HOST="$2"; shift ;;
        --dump1090-port) DUMP1090_PORT="$2"; shift ;;
        --stationid) STATIONID="$2"; shift ;;
        --content-mode) CONTENT_MODE="$2"; shift ;;
        install) ACTION="install" ;;
        uninstall) ACTION="uninstall" ;;
        update) ACTION="update" ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

case "$ACTION" in
    install)
         # Check for Connection String or Kafka Params
        if [[ -z "$CONNECTION_STRING" && ( -z "$KAFKA_BOOTSTRAP_SERVERS" || -z "$KAFKA_TOPIC" || -z "$SASL_USERNAME" || -z "$SASL_PASSWORD" ) ]]; then
            echo "Error: Provide either CONNECTION_STRING or all Kafka parameters (KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, SASL_USERNAME, SASL_PASSWORD)."
            exit 1
        fi

        # Check if required parameters are set
        if [[ -z "$STATIONID" ]]; then
            echo "Error: Station ID is required."
            exit 1
        fi
        if [[ -z "$ANTENNA_LAT" || -z "$ANTENNA_LON" ]]; then
            echo "Antenna latitude and longitude are required."
            exit 1
        fi
        install_service
        ;;
    uninstall)
        uninstall_service
        ;;
    update)
        update_service
        ;;
    *)
        echo "Usage: $0 {install|uninstall|update} [OPTIONS]"
        echo "Required parameters for install:"
        echo "  --antenna-lat <latitude>"
        echo "  --antenna-lon <longitude>"
        echo "  --dump1090-host <dump1090_host>"
        echo "  --dump1090-port <dump1090_port>"
        echo "  --stationid <stationid>"
        echo ""
        echo "Optional parameters:"
        echo "  --connection-string <conn_str>"
        echo "  --kafka-bootstrap-servers <servers>"
        echo "  --kafka-topic <topic>"
        echo "  --sasl-username <username>"
        echo "  --sasl-password <password>"
        echo "  --content-mode <structured|binary>"
        echo ""
        echo "Examples:"
        echo "  $0 install --antenna-lat 51.0 --antenna-lon 6.0 --dump1090-host localhost --dump1090-port 30005 --stationid station1"
        echo "  $0 uninstall"
        echo "  $0 update"
        exit 1
        ;;
esac
