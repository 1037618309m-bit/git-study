# 发钉钉消息
import requests

webhook = "https://oapi.dingtalk.com/robot/send?access_token=98e33568c28c2ad62504118c4abab1cbcc83e7544dd627441a9d8c1d119c9cef"

data = {
    "msgtype": "text",
    "text": {
        "content": "告警：张恩超注意你的言论！"
    }
}

response = requests.post(webhook, json=data)
print(response.text)

