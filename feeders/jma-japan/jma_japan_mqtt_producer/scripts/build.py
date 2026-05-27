import subprocess
import os

def main():
    packages = ["jma_japan_mqtt_producer_mqtt_client", "jma_japan_mqtt_producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()