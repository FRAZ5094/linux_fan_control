import subprocess

from fan_control import get_CPU_temp, get_GPU_temp


def get_fan_speeds():
    out = subprocess.Popen(
        ["liquidctl", "status"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    stdout, stderr = out.communicate()

    return stdout.decode("utf-8")


if __name__ == "__main__":
    print(get_fan_speeds())
    GPU_temp = get_GPU_temp()
    CPU_temp = get_CPU_temp()
    print(f"CPU temp: {CPU_temp}°C")
    print(f"GPU temp: {GPU_temp}°C")
