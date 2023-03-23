from machine import Pin, PWM
import time


p2 = PWM(Pin(15))
p2.freq(50)

# 0度   p2.duty_u16(1638)
# 90度  p2.duty_u16(4915)
# 180度 p2.duty_u16(8192)

for i in range(2):
    p2.duty_u16(1638)
    time.sleep(1)
    p2.duty_u16(4915)
    time.sleep(1)
    p2.duty_u16(8192)
    time.sleep(1)

for i in range(1638, 8192, 10):
    p2.duty_u16(i)
    time.sleep_ms(10)
