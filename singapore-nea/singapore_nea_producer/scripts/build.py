import subprocess
import os

def main():
    packages = ["singapore_nea_producer_kafka_producer", "singapore_nea_producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()