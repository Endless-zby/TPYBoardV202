from pushdeerUtil import PushDeer
import requests
import datetime
# pushdeer = PushDeer(pushkey="PDU1TtRhwbxSrMmJ38D4aPOduQdG82WcXOHVa")
# pushdeer.send_text(method="post", text="hello world", desp="optional description")


def send_pusher(key, result):
    urltxt = "http://192.168.192.36:8801/message/push?pushkey={}&text={}".format(key, result)
    return requests.get(url=urltxt)


if __name__ == "__main__":
    key = "PDU1TtRhwbxSrMmJ38D4aPOduQdG82WcXOHVa"  # 填写key密钥
    result = str(datetime.date.today()) + ' | python推送测试成功！'
    a = send_pusher(key, result)
    print(a)