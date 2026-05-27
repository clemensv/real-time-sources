import subprocess
import os

def main():
    packages = ["waterinfo_vmm_mqtt_producer_mqtt_client", "waterinfo_vmm_mqtt_producer_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()