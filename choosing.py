from fan_control import get_profile


profiles=get_profile()
CPU_profile=profiles["CPU"]
GPU_profile=profiles["GPU"]

CPU_temp=55
GPU_temp=73

for key in sorted(CPU_profile,reverse=True):
    if CPU_temp>=int(key):
        CPU_duty=key
        break


for key in sorted(GPU_profile,reverse=True):
    if GPU_temp>=int(key):
        GPU_duty=key
        break

print("CPU", CPU_duty)
print("GPU", GPU_duty)
print("max= ",max(GPU_duty,CPU_duty))