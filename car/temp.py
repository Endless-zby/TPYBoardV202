import socket  # 导入socket通信库
import machine
import requests
from machine import Pin
import network
import uasyncio as asyncio

# g4  和  g5 控制`左`边两个电机
# g12 和 g13 控制`右`边两个电机

# 网络设置
WIFI_SSID = "zby-2.4"
WIFI_PASSWORD = "zby123456"
PUSH_SERVER = "push.byzhao.cn:8801"
PUSH_KEY = "PDU1TtRhwbxSrMmJ38D4aPOduQdG82WcXOHVa"
UDP_PORT = 5005  # UDP服务器端口号


# 设置开发板的网络模式
wlan = network.WLAN(network.STA_IF)
wlan.active(True)  # 打开网络连接


def send_pusher(text, desp):
    urltxt = "http://{}/message/push?pushkey={}&text={}&desp={}".format(PUSH_SERVER, PUSH_KEY, text, desp)
    return requests.get(url=urltxt)


# 网络连接
def do_connect():  # 定义开发板连接无线网络的函数
    # oled_show([('Net connection...', 0, 20)])
    if not wlan.isconnected():  # 判断是否有网络连接
        print('connecting to network...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)  # 设置想要连接的无线名称和密码
        while not wlan.isconnected():  # 等待连接上无线网络
            pass
    print('network config:', wlan.ifconfig())


do_connect()
send_pusher('小车已上线', 'ip: ' + wlan.ifconfig()[0])
# 初始化UDP连接
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((wlan.ifconfig()[0], UDP_PORT))

# 电机驱动板
IN1 = Pin(4, Pin.OUT)  # 左前
IN2 = Pin(5, Pin.OUT)  # 左后
IN3 = Pin(12, Pin.OUT)  # 右前
IN4 = Pin(13, Pin.OUT)  # 右后


def go():
    IN1.value(1)
    IN2.value(0)
    IN3.value(1)
    IN4.value(0)


def back():
    IN1.value(0)
    IN2.value(1)
    IN3.value(0)
    IN4.value(1)


def left():
    IN1.value(0)
    IN2.value(1)
    IN3.value(1)
    IN4.value(0)


def right():
    IN1.value(1)
    IN2.value(0)
    IN3.value(0)
    IN4.value(1)


def stop():
    IN1.value(0)
    IN2.value(0)
    IN3.value(0)
    IN4.value(0)


while True:
    data, addr = sock.recvfrom(1024)
    data_str = data.decode("utf-8")
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


