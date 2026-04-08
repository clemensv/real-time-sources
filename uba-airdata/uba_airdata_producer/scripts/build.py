import subprocess
import os

def main():
    packages = ["uba_airdata_producer_kafka_producer", "uba_airdata_producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()