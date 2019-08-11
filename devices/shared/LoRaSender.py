from time import sleep
from ssd1306 import SSD1306_I2C
from machine import Pin, I2C

def send(lora):
    counter = 0
    print("LoRa Sender")
    #display = Display()

    rst = Pin(16, Pin.OUT)
    rst.value(1)
    scl = Pin(15, Pin.OUT, Pin.PULL_UP)
    sda = Pin(4, Pin.OUT, Pin.PULL_UP)
    i2c = I2C(scl=scl, sda=sda, freq=450000)
    oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

    def draw(message1, message2):
        oled.fill(0)
        oled.text('SENDER', 5, 5)
        oled.text('----------------------', 5, 20)
        oled.text(message1, 0, 35)
        oled.text(message2, 0, 50)
        oled.show()

    while True:
        payload = 'Hello ({0})'.format(counter)
        print("Sending packet: \n{}\n".format(payload))
        draw("{0}".format(payload), "RSSI: {0}".format(lora.packetRssi()))

        lora.println(payload)

        counter += 1
        sleep(1)
