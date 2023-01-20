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
# 超声波传感器Echo、Trig定义
Trig = Pin(5, Pin.OUT)
Echo = Pin(4, Pin.IN)

# 标准门距
door_dist = 1


wlan = network.WLAN(network.STA_IF)  # 设置开发板的网#络模式
wlan.active(True)  # 打开网络连接


# 呼吸灯(利用正余弦函数的周期性变化调节led亮度)
def respiration_led(led_, time_):
    for i in range(20):
        led_.duty(int(math.sin(i / 10 * math.pi) * 500 + 500))
        time.sleep_ms(time_)


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
            if recive.find('YES') > -1:
                print('Send Data OK')
        else:  # 数据发送完成，退出while
            break
    s.close()  # 关闭数据连接


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


def show_ip():
    oled_show([('ip: ', 0, 20), (wlan.ifconfig()[0], 0, 40)])



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
def temperature_measure(show_oled, send_server):
    d.measure()  # 调用DHT类库中测量数据的函数
    temp_ = str(d.temperature())  # 读取measure()函数中的温度数据
    hum_ = str(d.humidity())  # 读取measure()函数中的湿度数据
    # print('eg:', temp_, '-', hum_)
    if show_oled:
        # 测量数据oled显示
        oled_show([('temperature: ' + temp_, 0, 10), ('humidity: ' + hum_ + '%', 0, 30), ('dataBy: byzhao', 17, 50)])
    if send_server:
        # http_get('http://py.byzhao.cn/py/temperature?temperature=' + temp_ + '&humidity=' + hum_ + '')
        bt = '温度：{}℃  ----  湿度：{}%  ---- 当前时间：{}'.format(temp_, hum_, str(time.time()))
        udp_send(bt)


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
        return distance


def init_door():
    # 计算当前位置到门的距离 作为基准值，考虑误差 基准值 +-0.5cm属于合理区间
    dist = distance_measurement()
    # 修改全局变量door_dist
    global door_dist
    door_dist = range(dist - 0.5, dist + 0.5)


# 获取基准值范围
init_door()

# 核心方法
# 使整个函数应该在一个可控的周期内执行，应该要能调整这个周期的频率   int(math.sin(x * i))  0<i<5
# 可以将整个代码的执行过程作为一个正弦函数，在波峰对环境温度湿度做采样
# 在x轴奇数点对舱门状态做判断并计时
#
while True:  # 开始整个代码的大循环

    # 检测环境温度、湿度并上报 oled 或者 udp
    temperature_measure(True, True)

    # 超声波传感器检测门是否打开
    distance = distance_measurement()
    if distance in door_dist:
        oled_show([('舱门状态: 关闭', 0, 40)])
        # 灯灭
        led_blue.off()
    else:
        oled_show([('舱门状态: 打开', 0, 40)])
        # 灯亮
        led_blue.on()
        time.time_ns()
    # 计时 胖胖进入猫砂盆的时间




    # 对胖胖尿尿和拉屎时的空气湿度变化做一个分布图，通过湿度来判断是尿尿还是拉屎

    # 计算停留时间并上报

    # 接通继电器用风扇换气
