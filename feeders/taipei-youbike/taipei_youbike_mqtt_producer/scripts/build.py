import subprocess
import os

def main():
    packages = ["taipei_youbike_mqtt_producer_mqtt_client", "taipei_youbike_mqtt_producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()