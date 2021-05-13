import json
import os 


def get_temp():
    temp=input("Temp: ")
    return int(temp)

def get_profile():
    if os.path.exists("fan_profile.json"):
        with open("fan_profile.json", "r") as f:
            profile = json.load(f)
            return profile
    else:
        print("no fan profile")
def set_temp(temp):
    print("temp set to: ",temp)

while True:
    temp=get_temp()
    profile=get_profile()
    for key in sorted(profile,reverse=True):
        if temp>75:
            set_temp(100)
            break
        elif temp>=int(key):
            set_temp(profile[key])
            break

