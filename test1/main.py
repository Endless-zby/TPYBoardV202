import dht
import machine
from ssd1306 import SSD1306_I2C
import time, math  # 声明用到的类库，尤其是dht的类库
from machine import Pin, I2C



# 温湿度传感器data串口
d = dht.DHT11(machine.Pin(14))  # 声明用到类库中的函数，并设置参数


i2c = I2C(scl=Pin(5), sda=Pin(4))
oled = SSD1306_I2C(128, 64, i2c)


# oled显示函数
def oled_show(key):
    oled.fill(0)  # 清屏
    # print(len(key))
    for ss in key:
        # print(ss)
        ele = ss[0]
        x = ss[1]
        y = ss[2]
        oled.text(ele, x, y)
    oled.show()

# 温湿度传感器
def temperature_measure(show_oled):
    d.measure()  # 调用DHT类库中测量数据的函数
    temp_ = str(d.temperature())  # 读取measure()函数中的温度数据
    hum_ = str(d.humidity())  # 读取measure()函数中的湿度数据
    # print('eg:', temp_, '-', hum_)
    if show_oled:
        # 测量数据oled显示
        oled_show([('temperature: ' + temp_, 0, 10), ('humidity: ' + hum_ + '%', 0, 30), ('dataBy: byzhao', 17, 50)])


while True:  # 开始整个代码的大循环

    # 检测环境温度、湿度并上报 oled 或者 udp
    temperature_measure(True)
    time.sleep(2)


