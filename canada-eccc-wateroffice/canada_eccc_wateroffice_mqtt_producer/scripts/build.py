import subprocess
import os

def main():
    packages = ["canada_eccc_wateroffice_mqtt_producer_mqtt_client", "canada_eccc_wateroffice_mqtt_producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()