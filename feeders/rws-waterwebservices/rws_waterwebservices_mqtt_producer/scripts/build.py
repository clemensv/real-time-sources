import subprocess
import os

def main():
    packages = ["rws_waterwebservices_mqtt_producer_mqtt_client", "rws_waterwebservices_mqtt_producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()