import dht
import machine
import socket
from ssd1306 import SSD1306_I2C
import network
import time, math  # 声明用到的类库，尤其是dht的类库
from machine import Pin, I2C

# 温湿度传感器data串口
d = dht.DHT11(machine.Pin(14))  # 声明用到类库中的函数，并设置参数

servo = machine.PWM(machine.Pin(15), freq=50)
i2c = I2C(scl=Pin(5), sda=Pin(4))
oled = SSD1306_I2C(128, 64, i2c)

# 超声波传感器Echo、Trig定义
Trig = Pin(12, Pin.OUT)
Echo = Pin(13, Pin.IN)

wlan = network.WLAN(network.STA_IF)  # 设置开发板的网#络模式
wlan.active(True)  # 打开网络连接


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


# 网络连接
def do_connect():  # 定义开发板连接无线网络的函数
    oled_show([('Net connection...', 0, 20)])
    if not wlan.isconnected():  # 判断是否有网络连接
        print('connecting to network...')
        wlan.connect('blog-2.4', 'zby123456')  # 设置想要连接的无线名称和密码
        while not wlan.isconnected():  # 等待连接上无线网络
            pass
    # oled_text('Network connected!', 0, 20)
    oled_show([('Net connected!', 0, 20)])
    oled_show([('ip: ', 0, 20), (wlan.ifconfig()[0], 0, 40)])
    time.sleep(2)
    # oled_text('ip: ', 0, 20)
    # oled_text(wlan.ifconfig()[0], 0, 30)
    print('network config:', wlan.ifconfig())


do_connect()  # 连接无线网络

# udp网络配置
ip_address = '192.168.123.255'  # 广播地址
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 初始化socket
PORT = 8888  # 广播端口
server_address = (ip_address, PORT)
oled_show([('socket init ok!', 0, 20)])


# udp协议的信息上报
def udp_send(msg):
    # print(str(msg, 'utf8'), end='')
    client_socket.sendto(bytes(msg, 'utf-8'), server_address)


def sg90(du):
    t1 = 0.5 + 2 / 180 * du  # 范围2ms 角度180度 起始0.5ms
    pulse = int(t1 / 20 * 1023)
    print('移动的角度:', du, pulse)

    # servo.duty(77)
    servo.duty(pulse)  # 舵机角度的设定
    print('eg:', pulse)


# 温湿度传感器和距离传感器
def temperature_measure(show_oled, send_server):
    d.measure()  # 调用DHT类库中测量数据的函数
    temp_ = str(d.temperature())  # 读取measure()函数中的温度数据
    hum_ = str(d.humidity())  # 读取measure()函数中的湿度数据
    distance = distance_measurement()
    # print('eg:', temp_, '-', hum_)
    if show_oled:
        # 测量数据oled显示
        oled_show([('temperature: ' + temp_, 0, 10), ('humidity: ' + hum_ + '%', 0, 30), ('dataBy: byzhao', 17, 50)])
    if send_server:
        # http_get('http://py.byzhao.cn/py/temperature?temperature=' + temp_ + '&humidity=' + hum_ + '')
        # bt = '温度：{}℃  ----  湿度：{}%  ---- 当前时间：{}'.format(temp_, hum_, str(time.time()))
        bt = '{"temperature":' + temp_ + ',"humidity":' + hum_ + ',"distance":' + str(distance) + '}'
        udp_send(bt)
    if d.humidity() < 40:
        sg90(180)
    else:
        sg90(0)


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
        # 计算得到高电平持续时间 单位：us
        tc = te - ts
        # 根据音速计算距离（换算cm）  0.0343厘米/微秒
        distance = (tc * 0.0343) / 2
        print('Distance:', distance, '(cm)')
        # oled_show([('measurement: ' + distance, 0, 20)])
        return distance
        # bt = '测距数据：{}（cm）'.format(distance)
        # udp_send(bt)


while True:  # 开始整个代码的大循环

    # 检测环境温度、湿度并上报 oled 或者 udp
    temperature_measure(True, True)
    time.sleep(1)

    # time.sleep(2)
