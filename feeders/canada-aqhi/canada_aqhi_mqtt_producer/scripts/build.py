import subprocess
import os

def main():
    packages = ["canada_aqhi_mqtt_producer_mqtt_client", "canada_aqhi_mqtt_producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()