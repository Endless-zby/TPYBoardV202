# 全局变量
num = 10


def demo1():
    # 希望修改全局变量的值
    # 使用global关键字声明一下变量即可，global关键字会告诉解释器后面的变量是一个全局变量
    # 再使用赋值语句，就不会创建局部变量
    global num
    num = 47
    print("demo1==>num = %d" % num)


def demo2():
    print("demo2==>num = %d" % num)


demo1()
demo2()