import subprocess
import os

def main():
    packages = ["sensor_community_producer_kafka_producer", "sensor_community_producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()