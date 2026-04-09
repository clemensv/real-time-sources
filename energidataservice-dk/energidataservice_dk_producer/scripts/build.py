import subprocess
import os

def main():
    packages = ["energidataservice_dk_producer_kafka_producer", "energidataservice_dk_producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()