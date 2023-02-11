
import socket
import time  # 声明用到的类库，尤其是dht的类库
from machine import Pin, I2C


# 超声波传感器Echo、Trig定义
Trig = Pin(12, Pin.OUT)
Echo = Pin(13, Pin.IN)


# 测距
def distance_measurement():
    # 高电平发送方波 持续20us
    Trig.value(1)
    time.sleep_us(20)
    Trig.value(0)
    # 侦听Echo串口有无输入高电平 没有的话接着发送方波
    while Echo.value() == 0:
        Trig.value(1)
        time.sleep_us(20)
        Trig.value(0)
    # 侦听到Echo电平升高
    if Echo.value() == 1:
        # 记录当前时间
        ts = time.ticks_us()

        while Echo.value() == 1:
            pass
        te = time.ticks_us()
        print('te:{}, ts:{}', te, ts)
        # 计算得到高电平持续时间 单位：us
        tc = te - ts
        # 根据音速计算距离（换算cm）  0.0343厘米/微秒
        distance = (tc * 0.0343) / 2
        print('Distance:', distance, '(cm)')
        # oled_show([('measurement: ' + distance, 0, 20)])


while True:  # 开始整个代码的大循环

    # 检测环境温度、湿度并上报 oled 或者 udp
    distance_measurement()
    time.sleep(1)
    # distance_measurement()
    # time.sleep(2)

