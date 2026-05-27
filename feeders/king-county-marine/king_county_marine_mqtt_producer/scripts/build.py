import subprocess
import os

def main():
    packages = ["king_county_marine_mqtt_producer_mqtt_client", "king_county_marine_mqtt_producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()