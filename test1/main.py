import dht
import machine
from ssd1306 import SSD1306_I2C
import time, math  # 声明用到的类库，尤其是dht的类库
from machine import Pin, I2C

# 超声波传感器Echo、Trig定义
Trig = Pin(12, Pin.OUT)
Echo = Pin(13, Pin.IN)

# 温湿度传感器data串口
d = dht.DHT11(machine.Pin(14))  # 声明用到类库中的函数，并设置参数
servo = machine.PWM(machine.Pin(15), freq=50)

i2c = I2C(scl=Pin(5), sda=Pin(4))
oled = SSD1306_I2C(128, 64, i2c)


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


def sg90(du):
    t1 = 0.5 + 2 / 180 * du  # 范围2ms 角度180度 起始0.5ms
    pulse = int(t1 / 20 * 1023)
    print('移动的角度:', du, pulse)

    # servo.duty(77)
    servo.duty(pulse)  # 舵机角度的设定
    print('eg:', pulse)


# 温湿度传感器
def temperature_measure(show_oled):
    d.measure()  # 调用DHT类库中测量数据的函数
    temp_ = str(d.temperature())  # 读取measure()函数中的温度数据
    hum_ = str(d.humidity())  # 读取measure()函数中的湿度数据
    # print('eg:', temp_, '-', hum_)
    if show_oled:
        # 测量数据oled显示
        oled_show([('temperature: ' + temp_, 0, 10), ('humidity: ' + hum_ + '%', 0, 30), ('dataBy: byzhao', 17, 50)])
    if d.humidity() < 180:
        sg90(int(d.humidity()))


while True:  # 开始整个代码的大循环

    # 检测环境温度、湿度并上报 oled 或者 udp
    temperature_measure(True)
    distance_measurement()
    time.sleep(4)


