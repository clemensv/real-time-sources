import subprocess
import os

def main():
    packages = ["noaa_nws_producer_kafka_producer", "noaa_nws_producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()