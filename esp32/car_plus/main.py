# 此main是测试超声波传感器、温湿度传感器、oled、舵机的一个综合demo实例
# 增加了电机控制芯片L298N，并为esp32供电
# 电池：12V
#


import dht
import machine
import ssd1306
import time, math  # 声明用到的类库，尤其是dht的类库
from machine import Pin, I2C, SoftI2C
import network
import socket  # 导入socket通信库
import urequests
import ujson

# 电机驱动芯片
# g13  和  g12 控制`左`边两个电机
# g14 和 g27 控制`右`边两个电机
# IN1 = Pin(13, Pin.OUT)  # D13
# IN2 = Pin(12, Pin.OUT)  # D12
IN1 = Pin(27, Pin.OUT)  # D27
IN2 = Pin(26, Pin.OUT)  # D26
IN3 = Pin(33, Pin.OUT)  # D33
IN4 = Pin(32, Pin.OUT)  # D32


# 超声波传感器Echo、Trig定义
Trig = Pin(15, Pin.OUT)  # D15
Echo = Pin(2, Pin.IN)  # D2

# 温湿度传感器data串口
d = dht.DHT11(machine.Pin(18))  # 声明用到类库中的函数，并设置参数
servo = machine.PWM(machine.Pin(19), freq=50)

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

# 设置网络模式
wlan = network.WLAN(network.STA_IF)
wlan.active(True)  # 打开网络连接 准备连接无线网络，（调试结束后更换为AP模式）


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
        return distance


# oled显示函数  封装  支持多组数据显示，受屏幕大小（64*128）像素限制，目前支持三行英文
# 对中文的支持：需要手动建立字体库，根据1306驱动直接操作oled控制芯片
# 如果有屏幕画图需求阅读README.md
def oled_show(key):
    oled.fill(0)  # 先清屏
    # print(len(key))
    for ss in key:
        # print(ss)
        ele = ss[0]
        x = ss[1]
        y = ss[2]
        oled.text(ele, x, y)
    oled.show()


oled_show([('car start...', 0, 20)])


# 推送关键消息到手机， 例如系统上线、障碍物卡死、设备ip地址、ap模式下的设备接入情况，以及其他必要信息
def send_pusher(text, desp):
    body = {'text': text, 'desp': desp, 'pushkey': PUSH_KEY}
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    urltxt = "http://192.168.123.36:8801/message/push?pushkey={}&text={}&desp={}".format(PUSH_KEY, text, desp)
    response = urequests.post('http://192.168.123.36:8801/message/push', data=ujson.dumps(body), headers=headers)
    print('push:', urltxt)
    print(response.text)


# pwm控制舵机转向角度，通过计算控制一个周期内的空占比来使舵机转动指定的角度
def sg90(du):
    t1 = 0.5 + 2 / 180 * du  # 范围2ms 角度180度 起始0.5ms
    pulse = int(t1 / 20 * 1023)
    print('移动的角度:', du, pulse)
    servo.duty(pulse)  # 舵机角度的设定
    print('eg:', pulse)


# 温湿度传感器
# 周期性读取温湿度传感器的测量数据
# 舵机转动角度等于当前空气湿度（湿度的变化比较容易模拟）
def temperature_measure(show_oled):
    d.measure()  # 调用DHT类库中测量数据的函数
    temp_ = str(d.temperature())  # 读取measure()函数中的温度数据
    hum_ = str(d.humidity())  # 读取measure()函数中的湿度数据
    # print('eg:', temp_, '-', hum_)
    if show_oled:
        # 测量数据oled显示
        oled_show([('temperature: ' + temp_, 0, 10), ('humidity: ' + hum_ + '%', 0, 30), ('dataBy: byzhao', 17, 50)])


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


# 连接网络
do_connect()

# 发送当前设备ip地址
send_pusher('online', 'ip: ' + wlan.ifconfig()[0])
# 初始化UDP连接
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((wlan.ifconfig()[0], UDP_PORT))


# 设备移动
def go(millis):
    print('go')
    IN1.value(1)
    IN2.value(0)
    IN3.value(1)
    IN4.value(0)
    if millis != -1:
        print('go---')
        time.sleep(millis)  # 延时
        stop()
    else:
        pass


sg90(90)


def back(millis):
    print('back')
    IN1.value(0)
    IN2.value(1)
    IN3.value(0)
    IN4.value(1)
    if millis != -1:
        time.sleep(millis)  # 延时
        stop()
    else:
        pass


def left(millis):
    print('left')
    IN1.value(0)
    IN2.value(1)
    IN3.value(1)
    IN4.value(0)
    if millis != -1:
        time.sleep(millis)  # 延时
        stop()
    else:
        pass


def right(millis):
    print('right')
    IN1.value(1)
    IN2.value(0)
    IN3.value(0)
    IN4.value(1)
    if millis != -1:
        time.sleep(millis)  # 延时
        stop()
    else:
        pass


def stop():
    print('stop')
    IN1.value(0)
    IN2.value(0)
    IN3.value(0)
    IN4.value(0)


# 当前运动模式  默认是手动控制
auto_mode = False

while True:
    # 切换【自动控制】模式
    data, addr = sock.recvfrom(1024)
    data_str = data.decode("utf-8")
    # if len(data_str) > 0 & data_str == 'controller':
    #     global auto_mode
    #     auto_mode = ~auto_mode

    # go(-1)

    if auto_mode:
        # 当前是【自动控制】模式
        # 设置舵机方向为90°

        # 读取前方障碍物距离
        distance = distance_measurement()
        # 当距离小于20cm时停止
        if distance < 10:
            stop()
            sg90(90)
            distance_list = []
            # 从0°到180°角度检测距离前方障碍物的距离 10°取一次数据
            for jiaodu in range(0, 180, 10):
                print(jiaodu)
                sg90(jiaodu)
                distance = distance_measurement()
                distance_list.append(distance)
                time.sleep(0.5)
            # 收集完成18组方向距离数据 恢复舵机初始方向
            print(distance_list)
            # 计算当前位置右侧十八组数据
            max_value = max(distance_list)
            jiaodu = distance_list.index(max(distance_list)) * 10
            print('------')
            print(max_value)
            print(jiaodu)
            print('------')
            # 计算设备转动角度和时间的关系（后面用陀螺仪解决这个问题）  目前假设转动1°需要耗时8.3ms 即 0.0083秒
            if jiaodu < 90:
                left((90 - jiaodu) * 0.0083)
            else:
                right((jiaodu - 90) * 0.0083)
        else:
            pass
        sg90(90)
        time.sleep(1)
    else:
        # 当前是【手动控制】模式
        if data_str == 'forward':
            go(-1)
        elif data_str == 'backward':
            back(-1)
        elif data_str == 'left':
            left(-1)
        elif data_str == 'right':
            right(-1)
        else:
            stop()
