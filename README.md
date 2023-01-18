# 智能猫砂盆

> TPYBoardV202
> 开发环境：python
###  1、移动检测（_加速度传感器_）
###  2、温湿度检测（_温湿度传感器_）
###  3、距离检测（_超声波传感器_）

|TPYBoard v202|超声波模块（HC-SR04）|
|-------------|-------------------|
|+5V |Vcc|
|G14| Trig|
|G15| Echo|
|GND|Gnd|
- 工作原理

(1) 采用IO口Trig触发测距，给最少10us的高电平信号。

(2) 模块自动发送 8 个 40khz 的方波，自动检测是否有信号返回。

(3) 有信号返回，通过 IO 口 Echo 输出一个高电平，高电平持续的时间就是超声波从发射到返回的时间。测试距离=(高电平时间*声速(340M/S))/2。

- 代码实例

```python
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
        # 根据音速计算距离（换算cm）常温常压下 0.0343厘米/微秒
        distance = (tc * 0.0343) / 2
        print('Distance:', distance, '(cm)')
```
- 误差分析
> 超声波的传播速度受空气的密度所影响，空气的密度越高则超声波的传播速度就越快，而空气的密度又与温度有着密切的关系

超声波`速度与温度`的关系近似公式为：_C=C0+0.607×T℃ (C0为零度时的声波速度332m/s)_

###  4、猫砂盆门控制（_舵机_）
###  5、猫砂自动清筛（_步进电机_、_带减速器电机_、_滑轨_、_皮带_）
###  6、本地监控显示器（_0.96寸OLED显示屏_）
> 常用方法

|方法|解释|
|---|---|
|text(string, x, y)|在(x, y)处显示字符串，注意text()函数内置的字体是8x8的，暂时不能替换|
|poweroff()|关闭OLED显示|
|poweron()|空函数，无任何效果。可以用 write_cmd(0xAF) 代替|
|fill(n)|n=0，清空屏幕，n大于0，填充屏幕|
|contrast()|调整亮度。0最暗，255最亮|
|invert()|奇数时反相显示，偶数时正常显示|
|pixel(x, y, c)|在(x, y)处画点|
|show()|更新显示内容。前面大部分函数只是写入数据到缓冲区，并不会直接显示到屏幕，需要调用show()后才能显示出来。|
|framebuf.line(x1,y1,x2,y2,c)|画直线|
|framebuf.hline(x,y,w,c)|画水平直线|
|framebuf.vline(x,y,w,c)|画垂直直线|
|framebuf.fill_rect(x,y,w,h,c)|画填充矩形|
|framebuf.rect(x,y,w,h,c)|画空心矩形|
###  7、远程状态监控（_Lua或Java或python开发_）
###  8、无线传输（_板载wifi模块_）
###  9、远程控制协议（_客户端加密的UDP协议_）



### ESP8266引脚图

![ESP8266引脚图](resource/esp8266.png)



# PushDeer
> `PushDeer`可以将消息推送到各种支持MQTT协议的智能设备。  
> DeerESP 是 PushDeer 在 IOT 方向的扩展项目，它是一个基于 ESP8266/ESP32 芯片的消息设备方案。  
> 开发环境：arduino  
> DIE下载：https://www.arduino.cc/en/software  
> 1.44TFT资料：http://www.lcdwiki.com/zh/1.44inch_SPI_Arduino_Module_Black_SKU:MAR1442  

### ESP8266与1.44TFT

![ESP8266引脚图](resource/esp8266+1.44.png)

### 开发流程

- 由于我们使用的8266并没有内置到 ardunio IDE 中，我们还需要进行一下配置，在设置界面填上附加开发板管理器网址：
> esp8266 填写这个 https://arduino.esp8266.com/stable/package_esp8266com_index.json  
> esp32 填写这个 https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json  

