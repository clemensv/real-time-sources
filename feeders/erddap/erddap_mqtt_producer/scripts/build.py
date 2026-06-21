import subprocess
import os

def main():
    packages = ["erddap_mqtt_producer_mqtt_client", "erddap_mqtt_producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()