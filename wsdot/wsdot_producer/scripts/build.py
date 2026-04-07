import subprocess
import os

def main():
    packages = ["wsdot_producer_kafka_producer", "wsdot_producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()