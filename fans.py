from liquidctl import find_liquidctl_devices

# find all connected and supported devices
def set_speed(devices,percent,first):
    for dev in devices:
        with dev.connect():
            if first:
                init_status = dev.initialize()
            if "Corsair Commander Pro" in dev.description:
                dev.set_fixed_speed("sync", percent)
                print("Commander Pro set to", percent)
            elif "Corsair Hydro" in dev.description:
                if first:
                    dev.initialize(pump_mode='balanced')

                dev.set_fixed_speed("fan1", percent)
                dev.set_fixed_speed("fan2", percent)
                print("Hydro set to", percent)
