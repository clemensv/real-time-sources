import subprocess
import os

def main():
    packages = ["aviationweather_mqtt_producer_mqtt_client", "aviationweather_mqtt_producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()