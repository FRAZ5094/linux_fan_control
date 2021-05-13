import json
import os 
from liquidctl import find_liquidctl_devices
from get_temp import get_CPU_temp,get_GPU_temp
from fans import set_speed
from time import sleep

def get_profile():
    if os.path.exists("fan_profile.json"):
        with open("fan_profile.json", "r") as f:
            profile = json.load(f)
            return profile
    else:
        print("no fan profile")

if __name__ == "__main__":
    first=True
    devices_gen=find_liquidctl_devices()
    devices=[]
    for dev in devices_gen:
        devices.append(dev)

    last_duty=0

    while True:
        try:
            CPU_temp=get_CPU_temp()
            print("CPU_temp: ",CPU_temp)
            GPU_temp=get_GPU_temp()
            print("GPU_temp: ",GPU_temp)
            profiles=get_profile()
            CPU_profile=profiles["CPU"]
            GPU_profile=profiles["GPU"]

            for key in sorted(CPU_profile,reverse=True):
                if CPU_temp>=int(key):
                    CPU_duty=CPU_profile[key]
                    break
            for key in sorted(GPU_profile,reverse=True):
                if GPU_temp>=int(key):
                    GPU_duty=GPU_profile[key]
                    break
            duty=max(GPU_duty,CPU_duty)

            if CPU_temp>75 or GPU_temp>80:
                set_speed(devices,100,first)
                first=False
            else:
                if last_duty!=duty:
                    set_speed(devices,duty,first)
                    last_duty=duty
                else:
                    print("duty doesn't need to be changed")
                first=False
        except:
            pass
        sleep(2)
