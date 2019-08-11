
import time
import framebuf
from micropython import const
from machine import Pin, I2C

# register definitions
SET_CONTRAST        = const(0x81)
SET_ENTIRE_ON       = const(0xa4)
SET_NORM_INV        = const(0xa6)
SET_DISP            = const(0xae)
SET_MEM_ADDR        = const(0x20)
SET_COL_ADDR        = const(0x21)
SET_PAGE_ADDR       = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP       = const(0xa0)
SET_MUX_RATIO       = const(0xa8)
SET_COM_OUT_DIR     = const(0xc0)
SET_DISP_OFFSET     = const(0xd3)
SET_COM_PIN_CFG     = const(0xda)
SET_DISP_CLK_DIV    = const(0xd5)
SET_PRECHARGE       = const(0xd9)
SET_VCOM_DESEL      = const(0xdb)
SET_CHARGE_PUMP     = const(0x8d)

class SSD1306:
    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        # Note the subclass must initialize self.framebuf to a framebuffer.
        # This is necessary because the underlying data buffer is different
        # between I2C and SPI implementations (I2C needs an extra byte).
        self.poweron()
        self.init_display()

    def init_display(self):
        for cmd in (
            SET_DISP | 0x00, # off
            # address setting
            SET_MEM_ADDR, 0x00, # horizontal
            # resolution and layout
            SET_DISP_START_LINE | 0x00,
            SET_SEG_REMAP | 0x01, # column addr 127 mapped to SEG0
            SET_MUX_RATIO, self.height - 1,
            SET_COM_OUT_DIR | 0x08, # scan from COM[N] to COM0
            SET_DISP_OFFSET, 0x00,
            SET_COM_PIN_CFG, 0x02 if self.height == 32 else 0x12,
            # timing and driving scheme
            SET_DISP_CLK_DIV, 0x80,
            SET_PRECHARGE, 0x22 if self.external_vcc else 0xf1,
            SET_VCOM_DESEL, 0x30, # 0.83*Vcc
            # display
            SET_CONTRAST, 0xff, # maximum
            SET_ENTIRE_ON, # output follows RAM contents
            SET_NORM_INV, # not inverted
            # charge pump
            SET_CHARGE_PUMP, 0x10 if self.external_vcc else 0x14,
            SET_DISP | 0x01): # on
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(SET_DISP | 0x00)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def show(self):
        x0 = 0
        x1 = self.width - 1
        if self.width == 64:
            # displays with width of 64 pixels are shifted by 32
            x0 += 32
            x1 += 32
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_framebuf()

    def fill(self, col):
        self.framebuf.fill(col)

    def pixel(self, x, y, col):
        self.framebuf.pixel(x, y, col)

    def scroll(self, dx, dy):
        self.framebuf.scroll(dx, dy)

    def text(self, string, x, y, col=1):
        self.framebuf.text(string, x, y, col)

    def hline(self, x, y, w, c=1):
        self.framebuf.hline(x, y, w, c)

    def vline(self, x, y, h, c=1):
        self.framebuf.vline(x, y, h, c)

    def line(self, x1, y1, x2, y2, c=1):
        self.framebuf.line(x1, y1, x2, y2, c)

    def rect(self, x, y, w, h, c=1):
        self.framebuf.rect(x, y, w, h, c)

    def fill_rect(self, x, y, w, h, c=1):
        self.framebuf.fill_rect(x, y, w, h, c)

class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c, addr=0x3c, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        # Add an extra byte to the data buffer to hold an I2C data/command byte
        # to use hardware-compatible I2C transactions.  A memoryview of the
        # buffer is used to mask this byte from the framebuffer operations
        # (without a major memory hit as memoryview doesn't copy to a separate
        # buffer).
        self.buffer = bytearray(((height // 8) * width) + 1)
        self.buffer[0] = 0x40  # Set first byte of data buffer to Co=0, D/C=1
        self.framebuf = framebuf.FrameBuffer1(memoryview(self.buffer)[1:], width, height)
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80 # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_framebuf(self):
        # Blast out the frame buffer using a single I2C transaction to support
        # hardware I2C interfaces.
        self.i2c.writeto(self.addr, self.buffer)

    def poweron(self):
        pass


#
# rst = Pin(16, Pin.OUT)
# rst.value(1)
# scl = Pin(15, Pin.OUT, Pin.PULL_UP)
# sda = Pin(4, Pin.OUT, Pin.PULL_UP)
# i2c = I2C(scl=scl, sda=sda, freq=450000)
# oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)


class Display:

    def __init__(self,
                 width = 128, height = 64,
                 scl_pin_id = 15, sda_pin_id = 4,
                 freq = 450000):

        self.width = width
        self.height = height
        self.poweron()
        self.i2c = I2C(scl = Pin(scl_pin_id, Pin.OUT),
                               sda = Pin(sda_pin_id),
                               freq = freq)
        self.display = SSD1306_I2C(width, height, self.i2c)
        self.show = self.display.show

    def poweron(self, pin=16):
        pin_reset = Pin(pin, mode=Pin.OUT)
        # pin_reset.value(0)
        # time.sleep_ms(50)
        pin_reset.value(1)

    def clear(self):
        self.display.fill(0)
        self.display.show()


    def show_text(self, text, x = 0, y = 0, clear_first = True, show_now = True, hold_seconds = 0):
        if clear_first: self.display.fill(0)
        self.display.text(text, x, y)
        if show_now:
            self.display.show()
            if hold_seconds > 0: time.sleep(hold_seconds)


    def wrap(self, text, start_line = 0,
             height_per_line = 8, width_per_char = 8,
             start_pixel_each_line = 0):

        chars_per_line = self.width//width_per_char
        max_lines = self.height//height_per_line - start_line
        lines = [(text[chars_per_line*line: chars_per_line*(line+1)], start_pixel_each_line, height_per_line*(line+start_line))
                 for line in range(max_lines)]

        return lines


    def show_text_wrap(self, text,
                       start_line = 0, height_per_line = 8, width_per_char = 8, start_pixel_each_line = 0,
                       clear_first = True, show_now = True, hold_seconds = 0):

        if clear_first: self.clear()

        for line, x, y in self.wrap(text, start_line, height_per_line, width_per_char, start_pixel_each_line):
            self.show_text(line, x, y, clear_first = False, show_now = False)

        if show_now:
            self.display.show()
            if hold_seconds > 0: time.sleep(hold_seconds)


    def show_datetime(self, year, month, day, hour, minute, second):
        datetime = [year, month, day, hour, minute, second]
        datetime_str = ["{0:0>2}".format(d) for d in datetime]

        self.show_text(text = '-'.join(datetime_str[:3]),
                        x = 0, y = 0, clear_first = True, show_now = False)
        self.show_text(text = ':'.join(datetime_str[3:6]),
                        x = 0, y = 10, clear_first = False, show_now = True)


    def show_time(self, year, month, day, hour, minute, second):
        self.show_datetime(year, month, day, hour, minute, second)
