import subprocess
import os

def main():
    packages = ["uk_bods_siri_producer_kafka_producer", "uk_bods_siri_producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()