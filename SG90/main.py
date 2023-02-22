import machine
import time

#设置PWM 引脚G5,频率50Hz
servo = machine.PWM(machine.Pin(15), freq=50)
du = 0
t1 = 0.5 + 2 / 180 * du   #范围2ms 角度180度 起始0.5ms
pulse = int(t1 / 20 * 1023)
print('移动的角度:', du, pulse)

# servo.duty(77)
servo.duty(pulse)#舵机角度的设定
print('eg:', pulse)

# time.sleep(2)#延时2秒
# servo.duty(110)
# print('eg:', 110)
# time.sleep(4)#延时2秒
# servo.duty(90)
# print('eg:', 90)
# servo.deinit()
