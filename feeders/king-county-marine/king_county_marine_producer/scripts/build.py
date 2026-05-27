import subprocess
import os

def main():
    packages = ["king_county_marine_producer_kafka_producer", "king_county_marine_producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()