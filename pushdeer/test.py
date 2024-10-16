
from pushdeerUtil import PushDeer
import requests
# import urequests
import datetime
# pushdeer = PushDeer(pushkey="PDU1TtRhwbxSrMmJ38D4aPOduQdG82WcXOHVa")
# pushdeer.send_text(method="post", text="hello world", desp="optional description")
BARK_URL = "http://192.168.192.208:8081/wuaFrBQHBvF25bbPEt69Mg/{}/{}"

# def send_pusher(key, result):
#     urltxt = "http://192.168.123.36:8801/message/push?desp=&pushkey={}&text={}&type=".format(key, result)
#     return requests.get(url=urltxt)

def send_bark(text, desp):
    urltxt = BARK_URL.format(text, desp)
    return requests.get(url=urltxt)

if __name__ == "__main__":
    # key = "PDU1TgQHPSWCR6tuX5UZJr1Lgs4gXT2yrKJTE"  # 填写key密钥
    # result = str(datetime.date.today()) + ' | python推送测试成功！'
    # a = send_pusher(key, result)

    send_bark("sodded", "Added")
