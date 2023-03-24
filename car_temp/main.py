import socket  # 导入socket通信库
import machine
import urequests
from ssd1306 import SSD1306_I2C
import network
from machine import Pin, I2C
import uasyncio as asyncio
import ujson,time

# g4  和  g5 控制`左`边两个电机
# g12 和 g13 控制`右`边两个电机

IN1 = Pin(4, Pin.OUT)  # D2
IN2 = Pin(5, Pin.OUT)  # D1
IN3 = Pin(12, Pin.OUT)  # D6
IN4 = Pin(13, Pin.OUT)  # D7

# 超声波传感器Echo、Trig定义
# Echo = Pin(15, Pin.OUT)  # D8
# Trig = Pin(3, Pin.IN)  # RX

servo = machine.PWM(machine.Pin(14), freq=50)  # D5

# i2c = I2C(scl=Pin(15), sda=Pin(14))
# i2c = I2C(scl=Pin(5), sda=Pin(4))
# oled = SSD1306_I2C(128, 64, i2c)

# 网络设置
WIFI_SSID = "blog-2.4"
WIFI_PASSWORD = "zby123456"
PUSH_KEY = "PDU1TgQHPSWCR6tuX5UZJr1Lgs4gXT2yrKJTE"
UDP_PORT = 5005  # UDP服务器端口号

# 设置开发板的网络模式
wlan = network.WLAN(network.STA_IF)
wlan.active(True)  # 打开网络连接


# oled显示函数
# def oled_show(key):
#     oled.fill(0)  # 清屏
#     # print(len(key))
#     for ss in key:
#         # print(ss)
#         ele = ss[0]
#         x = ss[1]
#         y = ss[2]
#         oled.text(ele, x, y)
#     oled.show()


def send_pusher(text, desp):
    body = {'text': text, 'desp': desp, 'pushkey': PUSH_KEY}
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    urltxt = "http://192.168.123.36:8801/message/push?pushkey={}&text={}&desp={}".format(PUSH_KEY, text, desp)
    response = urequests.post('http://192.168.123.36:8801/message/push', data=ujson.dumps(body), headers=headers)
    print('push:', urltxt)
    print(response)
    print(response.text)


# def distance_measurement():
#     # 高电平发送方波 持续20us
#     Trig.value(1)
#     time.sleep_us(20)
#     Trig.value(0)
#     # 侦听Echo串口有无输入高电平 没有的话接着发送方波
#     while Echo.value() == 0:
#         Trig.value(1)
#         time.sleep_us(20)
#         Trig.value(0)
#     # 侦听到Echo电平升高
#     if Echo.value() == 1:
#         # 记录当前时间
#         ts = time.ticks_us()
#
#         while Echo.value() == 1:
#             pass
#         te = time.ticks_us()
#         print('te:{}, ts:{}', te, ts)
#         # 计算得到高电平持续时间 单位：us
#         tc = te - ts
#         # 根据音速计算距离（换算cm）  0.0343厘米/微秒
#         distance = (tc * 0.0343) / 2
#         print('Distance:', distance, '(cm)')
#         # oled_show([('measurement: ' + distance, 0, 20)])


def sg90(du):
    t1 = 0.5 + 2 / 180 * du  # 范围2ms 角度180度 起始0.5ms
    pulse = int(t1 / 20 * 1023)
    print('移动的角度:', du, pulse)

    # servo.duty(77)
    servo.duty(pulse)  # 舵机角度的设定
    print('eg:', pulse)


# 网络连接
def do_connect():  # 定义开发板连接无线网络的函数
    # oled_show([('Net connection...', 0, 20)])
    if not wlan.isconnected():  # 判断是否有网络连接
        print('connecting to network...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)  # 设置想要连接的无线名称和密码
        while not wlan.isconnected():  # 等待连接上无线网络
            pass
        # oled_show([('ip: ', 0, 20), (wlan.ifconfig()[0], 0, 40)])
    print('network config:', wlan.ifconfig())


do_connect()

send_pusher('online', 'ip: ' + wlan.ifconfig()[0])
# 初始化UDP连接
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((wlan.ifconfig()[0], UDP_PORT))

sg90(90)


def go():
    print('go')
    sg90(90)
    IN1.value(1)
    IN2.value(0)
    IN3.value(1)
    IN4.value(0)


def back():
    print('back')
    sg90(45)
    IN1.value(0)
    IN2.value(1)
    IN3.value(0)
    IN4.value(1)


def left():
    print('left')
    sg90(180)
    IN1.value(0)
    IN2.value(1)
    IN3.value(1)
    IN4.value(0)


def right():
    print('right')
    sg90(0)
    IN1.value(1)
    IN2.value(0)
    IN3.value(0)
    IN4.value(1)


def stop():
    print('stop')
    IN1.value(0)
    IN2.value(0)
    IN3.value(0)
    IN4.value(0)


while True:
    data, addr = sock.recvfrom(1024)
    data_str = data.decode("utf-8")
    print('stop')
    if data_str == 'forward':
        go()
    elif data_str == 'backward':
        back()
    elif data_str == 'left':
        left()
    elif data_str == 'right':
        right()
    else:
        stop()
