import json
import subprocess
from time import sleep


def get_GPU_temp():
    out = subprocess.Popen(
        ["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    stdout, stderr = out.communicate()

    return int(stdout)


def get_CPU_temp():
    out = subprocess.Popen(
        ["sensors", "-j"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    stdout, stderr = out.communicate()
    data = json.loads(stdout)
    return int(data["zenpower-pci-00c3"]["Tdie"]["temp1_input"])


if __name__ == "__main__":
    while True:
        print("Getting temps")
        print("GPU temp: ", get_GPU_temp())
        print("CPU temp; ", get_CPU_temp())
        sleep(5)
