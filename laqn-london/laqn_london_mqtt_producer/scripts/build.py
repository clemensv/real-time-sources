import subprocess
import os

def main():
    packages = ["laqn_london_mqtt_producer_mqtt_client", "laqn_london_mqtt_producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()