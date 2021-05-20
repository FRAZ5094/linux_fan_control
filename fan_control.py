import json
import os
import subprocess
from time import sleep

from liquidctl import find_liquidctl_devices


def set_speed(devices, percent, first):
    for dev in devices:
        with dev.connect():
            # if first:
            # init_status = dev.initialize()
            if "Corsair Commander Pro" in dev.description:
                dev.set_fixed_speed("sync", percent)
                # print("Commander Pro set to", percent)
            elif "Corsair Hydro" in dev.description:
                # if first:
                # dev.initialize(pump_mode="balanced")

                dev.set_fixed_speed("fan1", percent)
                dev.set_fixed_speed("fan2", percent)
                # print("Hydro set to", percent)


def get_profile():
    if os.path.exists("fan_profile.json"):
        with open("fan_profile.json", "r") as f:
            profile = json.load(f)
            return profile
    else:
        print("no fan profile")


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
    try:
        subprocess.call("sudo liquidctl initialize all", shell=True, timeout=5)
    except Exception as e:
        print("failed to initialize")
        print("e")
    first = True
    devices_gen = find_liquidctl_devices()
    devices = []
    for dev in devices_gen:
        devices.append(dev)

    last_duty = 0

    while True:
        try:
            CPU_temp = get_CPU_temp()
            # print("CPU_temp: ", CPU_temp)
            GPU_temp = get_GPU_temp()
            # print("GPU_temp: ", GPU_temp)
            profiles = get_profile()
            CPU_profile = profiles["CPU"]
            GPU_profile = profiles["GPU"]

            for key in sorted(CPU_profile, reverse=True):
                if CPU_temp >= int(key):
                    CPU_duty = CPU_profile[key]
                    break
            for key in sorted(GPU_profile, reverse=True):
                if GPU_temp >= int(key):
                    GPU_duty = GPU_profile[key]
                    break
            duty = max(GPU_duty, CPU_duty)
            # print("duty: ", duty)
            if CPU_temp > 75 or GPU_temp > 80:
                set_speed(devices, 100, first)
                first = False
            else:
                if last_duty != duty:
                    set_speed(devices, duty, first)
                    last_duty = duty
                else:
                    pass
                    # print("duty doesn't need to be changed")
                first = False
        except:
            pass
        sleep(1)
