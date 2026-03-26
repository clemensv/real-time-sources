import subprocess
import os

def main():
    packages = ["hubeau_hydrometrie_producer_kafka_producer", "hubeau_hydrometrie_producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()