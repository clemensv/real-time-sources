import subprocess
import os

def main():
    packages = ["uk_ea_flood_monitoring_mqtt_producer_mqtt_client", "uk_ea_flood_monitoring_mqtt_producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()