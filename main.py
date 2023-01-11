import pyb
import dht
import machine
import network
import socket
from ssd1306 import SSD1306_I2C
from datetime import datetime
import urllib
import time, math  # 声明用到的类库，尤其是dht的类库

# 温湿度传感器data串口
d = dht.DHT11(machine.Pin(5))  # 声明用到类库中的函数，并设置参数
led_blue = machine.PWM(machine.Pin(2), freq=100)
# USR按键
sw=pyb.Switch()

# 呼吸灯(利用正余弦函数的周期性变化调节led亮度)
def respiration_led(led_, time_):
    for i in range(20):
        led_.duty(int(math.sin(i / 10 * math.pi) * 500 + 500))
        time.sleep_ms(time_)


def switch():
    sw_state = sw()
    if sw_state:
        print('USR被按下')
        led_blue.on()
    else:
        print('USR松开')
        led_blue.off()

# oled 显示屏驱动 长128 宽64
i2c = machine.I2C(-1, sda=machine.Pin(4), scl=machine.Pin(0), freq=100000)
oled = SSD1306_I2C(128, 64, i2c)


# def oled_text(str, x=40, y=30):
#     oled.text(str, x, y)
#     oled.show()


# oled显示函数
def oled_show(key):
    oled.fill(0)  # 清屏
    print(len(key))
    for ss in key:
        print(ss)
        ele = ss[0]
        x = ss[1]
        y = ss[2]
        oled.text(ele, x, y)
    oled.show()


# tcp
def http_get(url):  # 定义数据上传的函数
    _, _, host, path = url.split('/', 3)  # 分割传进来的参数
    addr = socket.getaddrinfo(host, 80)[0][-1]  # 把传进来的参数处理成符合格式的地址
    s = socket.socket()
    s.connect(addr)  # 链接地址
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))  # 向链接的地址发送数据
    while True:  # 开始数据发送
        data = s.recv(50)
        if data:  # 数据未发送完成，继续发送
            recive = str(data, 'utf8').upper()
            # print(str(data, 'utf8'), end='')
            if (recive.find('YES') > -1):
                print('Send Data OK')
        else:  # 数据发送完成，退出while
            break
    s.close()  # 关闭数据连接


# 网络连接
def do_connect():  # 定义开发板连接无线网络的函数
    oled_show([('Net connection...', 0, 20)])
    wlan = network.WLAN(network.STA_IF)  # 设置开发板的网#络模式
    wlan.active(True)  # 打开网络连接
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
    print(str(msg, 'utf8'), end='')
    client_socket.sendto(bytes(msg, 'utf-8'), server_address)


udp_send('系统上线！ 时间：' + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))


# 温湿度传感器
def temperature_measure(show_led, send_server):
    d.measure()  # 调用DHT类库中测量数据的函数
    temp_ = str(d.temperature())  # 读取measure()函数中的温度数据
    hum_ = str(d.humidity())  # 读取measure()函数中的湿度数据
    # print('eg:', temp_, '-', hum_)
    if show_led:
        # 测量数据oled显示
        oled_show([('temperature: ' + temp_, 0, 10), ('humidity: ' + hum_ + '%', 0, 30), ('dataBy: byzhao', 17, 50)])
    else:
        pass
    if send_server:
        # http_get('http://py.byzhao.cn/py/temperature?temperature=' + temp_ + '&humidity=' + hum_ + '')
        bt = '温度：{}℃  ----  湿度：{}%  ---- 当前时间：{}'.format(temp_, hum_, str(time.time()))
        udp_send(bt)
    else:
        pass


# 核心方法
while True:  # 开始整个代码的大循环

    # 检测环境温度、湿度并上报
    temperature_measure(True, True)

    # 超声波传感器检测门是否打开

    # 计时

    # 计算停留时间并上报

    # 接通继电器换气
