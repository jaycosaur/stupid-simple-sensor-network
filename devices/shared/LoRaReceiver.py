from ssd1306 import SSD1306_I2C
from machine import Pin, I2C
import time


def startup_view(screen):
    def star(x, y, w):
        screen.hline(x - w // 2, y, w)
        screen.vline(x, y - w // 2, w)
        screen.line(x - w // 2, y - w // 2, x + w // 2, y + w // 2)
        screen.line(x + w // 2, y - w // 2, x - w // 2, y + w // 2)

    for i in range(0, 6):
        star(15+24*i, 10, 10)
        star(5+24*i, 30, 10)
        star(15+24*i, 50, 10)

    screen.show()

    for i in range(0, 30):
        screen.scroll(4, 2)
        screen.show()
        time.sleep(0.05)


# char is 8x8 pixels wide
def display_view(screen, packet_rssi, message, thingy_id, time_sync):
    # clear display
    screen.fill(0)

    # header
    screen.vline(28, 0, 10)
    screen.vline(108, 0, 10)
    screen.hline(0, 10, 128)
    screen.text('REC', 0, 0)
    screen.text(thingy_id, 32, 0)
    screen.text("UP", 112, 0)

    # main body
    screen.text(message, 0, 12)
    screen.text("RSSI:{0}".format(packet_rssi), 0, 24)

    # footer
    screen.hline(0, 54, 128)
    screen.text("{}".format("OK"), 0, 56)
    screen.text("{}".format(time_sync), 48, 56)

    # update display
    screen.show()

def receive(lora):
    print("LoRa Receiver")
    rst = Pin(16, Pin.OUT)
    rst.value(1)
    scl = Pin(15, Pin.OUT, Pin.PULL_UP)
    sda = Pin(4, Pin.OUT, Pin.PULL_UP)
    i2c = I2C(scl=scl, sda=sda, freq=450000)
    oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

    last_sync_time = 1560668066
    time_last_sync = time.time()

    def get_estimated_time():
        return last_sync_time + time.time() - time_last_sync

    startup_view(oled)

    while True:
        if lora.receivedPacket():
            lora.blink_led()

            try:
                payload = lora.read_payload()
                display_view(oled, lora.packetRssi(), payload.decode(), "thing1", get_estimated_time())
                print("*** Received message ***\n{}".format(payload.decode()))

            except Exception as e:
                print(e)
