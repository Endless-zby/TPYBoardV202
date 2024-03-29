import socket  # 导入socket通信库
import machine
import urequests
import network
from machine import Pin, I2C, SoftI2C
import ujson
import ssd1306

# g13  和  g12 控制`左`边两个电机
# g14 和 g27 控制`右`边两个电机

IN1 = Pin(13, Pin.OUT)  # D13
IN2 = Pin(12, Pin.OUT)  # D12
IN3 = Pin(14, Pin.OUT)  # D14
IN4 = Pin(27, Pin.OUT)  # D27

# 超声波传感器Echo、Trig定义
Trig = Pin(15, Pin.OUT)  # D15
Echo = Pin(2, Pin.IN)  # D2

servo = machine.PWM(machine.Pin(19), freq=50)  # D19

# 创建i2c对象
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

# 宽度高度
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# 网络设置
WIFI_SSID = "blog-2.4"
WIFI_PASSWORD = "zby123456"
PUSH_KEY = "PDU1TgQHPSWCR6tuX5UZJr1Lgs4gXT2yrKJTE"
UDP_PORT = 5005  # UDP服务器端口号

# 设置开发板的网络模式
wlan = network.WLAN(network.STA_IF)
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


def send_pusher(text, desp):
    body = {'text': text, 'desp': desp, 'pushkey': PUSH_KEY}
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    urltxt = "http://192.168.123.36:8801/message/push?pushkey={}&text={}&desp={}".format(PUSH_KEY, text, desp)
    response = urequests.post('http://192.168.123.36:8801/message/push', data=ujson.dumps(body), headers=headers)
    print('push:', urltxt)
    print(response)
    print(response.text)


def sg90(du):
    t1 = 0.5 + 2 / 180 * du  # 范围2ms 角度180度 起始0.5ms
    pulse = int(t1 / 20 * 1023)
    print('移动的角度:', du, pulse)

    # servo.duty(77)
    servo.duty(pulse)  # 舵机角度的设定
    print('eg:', pulse)


# 网络连接
def do_connect():  # 定义开发板连接无线网络的函数
    oled_show([('Net connection...', 0, 20)])
    if not wlan.isconnected():  # 判断是否有网络连接
        print('connecting to network...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)  # 设置想要连接的无线名称和密码
        while not wlan.isconnected():  # 等待连接上无线网络
            pass
        oled_show([('ip: ', 0, 20), (wlan.ifconfig()[0], 0, 40)])
    print('network config:', wlan.ifconfig())


do_connect()

send_pusher('online', 'ip: ' + wlan.ifconfig()[0])
# 初始化UDP连接
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((wlan.ifconfig()[0], UDP_PORT))


def go():
    print('go')
    IN1.value(1)
    IN2.value(0)
    IN3.value(1)
    IN4.value(0)


def back():
    print('back')
    IN1.value(0)
    IN2.value(1)
    IN3.value(0)
    IN4.value(1)


def left():
    print('left')
    IN1.value(0)
    IN2.value(1)
    IN3.value(1)
    IN4.value(0)


def right():
    print('right')
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


# 当前小车的运动模式  默认是手动控制
auto_mode = False

while True:
    # 切换【自动控制】模式
    data, addr = sock.recvfrom(1024)
    data_str = data.decode("utf-8")
    if len(data_str) > 0 & data_str == 'controller':
        global auto_mode
        auto_mode = ~auto_mode

    if auto_mode:
        # 当前是【自动控制】模式
        # 设置舵机方向为90°
        sg90(90)
        # 读取前方障碍物距离

    else:
        # 当前是【手动控制】模式
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






