from machine import Pin
import time

"""
echo脚会由0变为1此时MCU开始计时，当超声波模块接收到返回的声波时，echo由1变为0此时MCU停止计时
然后再通过声音的传输速度是340m/s就可以计算出距离，切记要除以2，毕竟声音是来回的距离
"""


# https://doc.itprojects.cn/0006.zhishi.esp32/02.doc/index.html#/44.distance

def measure():
    # 告诉芯片要开始测试了
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    # 检测回响信号，为低电平时，测距完成
    while echo.value() == 0:
        # 开始不断递增的微秒计数器 1
        t1 = time.ticks_us()
    print("---------------------")
    print(t1)
    # 检测回响信号，为高电平时，测距开始
    while echo.value() == 1:
        # 开始不断递增的微秒计数器 2
        t2 = time.ticks_us()
    print(t2)

    # 计算两次调用 ticks_ms(), ticks_us(), 或 ticks_cpu()之间的时间，这里是ticks_us()
    # 这时间差就是测距总时间，在乘声音的传播速度340米/秒，除2就是距离
    # 例如 t2-t1=12848此时单位是us，转换为秒就是12848 / 1000000 此时单位是秒，此时如果乘以340计算出的单位是米，
    # 然后再乘以100就是厘米，因此，直接 用12848/10000即可
    t3 = time.ticks_diff(t2, t1) / 10000
    print(t3, t2 - t1)

    # 这里返回的是：开始测距的时间减测距完成的时间*声音的速度/2（来回）
    return t3 * 340 / 2


# 引脚设定
trig = Pin(15, Pin.OUT)
echo = Pin(2, Pin.IN)
trig.value(0)
echo.value(0)

# try/except语句用来检测try语句块中的错误，从而让except语句捕获异常信息并处理
try:
    while True:
        print("当前测量距离为:%0.2f cm" % measure())
        time.sleep(1)

except KeyboardInterrupt:
    pass
