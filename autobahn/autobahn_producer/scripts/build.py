import subprocess
import os

def main():
    packages = ["autobahn_producer_kafka_producer", "autobahn_producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()