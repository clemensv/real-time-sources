import subprocess
import os

def main():
    packages = ["gtfs_rt_producer_kafka_producer", "gtfs_rt_producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()