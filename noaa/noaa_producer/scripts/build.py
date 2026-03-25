import subprocess
import os

def main():
    packages = ["noaa-producer_kafka_producer", "noaa-producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()