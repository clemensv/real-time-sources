import subprocess
import os

def main():
    packages = ["french_road_traffic_producer_kafka_producer", "french_road_traffic_producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()