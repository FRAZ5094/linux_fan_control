from liquidctl import find_liquidctl_devices

# find all connected and supported devices
devices = find_liquidctl_devices()
dev_objects=[]
for dev in devices:
    dev_objects.append(dev)
    # connect to the device (here a context manager is used, but the
    # connection can also be manually managed)
    with dev.connect():
        if "Corsair Commander Pro" in dev.description:
            color1 = [[255,0,255]]
            #,[0,128,255]]

            color2=[[0,128,255]]
            dev.set_color("sync",mode="clear",colors=[])
            #dev.set_color('led1',"color_wave",colors=color1,start_led=1,maximum_leds=64,speed="fast")
            dev.set_color('led1',"fixed",colors=color2,start_led=1,maximum_leds=64)
            #print(dev.get_status())
            