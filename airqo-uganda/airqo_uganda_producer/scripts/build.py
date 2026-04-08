import subprocess
import os

def main():
    packages = ["airqo_uganda_producer_kafka_producer", "airqo_uganda_producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()