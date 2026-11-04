from flask import Flask, request
import requests
import json

app = Flask(__name__)

DINGTALK_WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=98e33568c28c2ad62504118c4abab1cbcc83e7544dd627441a9d8c1d119c9cef"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    text = "【告警】\n"
    for alert in data.get('alerts', []):
        text += f"告警名：{alert.get('labels', {}).get('alertname', '未知')}\n"
        text += f"级别：{alert.get('labels', {}).get('severity', '未知')}\n"
        text += f"描述：{alert.get('annotations', {}).get('description', '无')}\n"
    
    requests.post(DINGTALK_WEBHOOK, json={
        "msgtype": "text",
        "text": {"content": text}
    })
    
    return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

