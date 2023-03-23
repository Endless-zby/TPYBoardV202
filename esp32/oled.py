from machine import Pin, SoftI2C
from time import sleep
import ssd1306

# 创建i2c对象
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

# 宽度高度
oled_width = 128
oled_height = 64

# 创建oled屏幕对象
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# 在指定位置处显示文字
oled.text('Hello!', 0, 0)
oled.text('Hello, World 2!', 0, 10)
oled.text('Hello, World 3!', 0, 20)

oled.show()
