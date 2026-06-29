import subprocess
import os

def main():
    packages = ["hsl_hfp_upstream_mqtt_client", "hsl_hfp_upstream_data"]

    for package in packages:
        os.chdir(package)
        subprocess.run(["poetry", "build"], check=True)
        os.chdir("..")

if __name__ == "__main__":
    main()