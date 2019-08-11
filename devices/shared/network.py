def connect_to_wifi(ssid: str, password: str):
    import network
    sta = network.WLAN(network.STA_IF)
    if not sta.isconnected():
        print("connecting to %s wifi network ..." % ssid)
        sta.active(True)
        sta.connect(ssid, password)
        while not sta.isconnected():
            pass
        print('network config:', sta.ifconfig())
