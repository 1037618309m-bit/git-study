# 完整实战：读日志挑ERROR → 自动发钉钉告警
import requests

webhook = "https://oapi.dingtalk.com/robot/send?access_token=98e33568c28c2ad62504118c4abab1cbcc83e7544dd627441a9d8c1d119c9cef"

# 第一步：读日志，挑ERROR
with open("app.log", "r") as f:
    lines = f.readlines()

error_lines = []
for line in lines:
    line = line.strip()
    if "ERROR" in line:
        error_lines.append(line)

# 第二步：如果有ERROR，发钉钉告警
if len(error_lines) > 0:
    error_text = "\n".join(error_lines)
    content = f"告警：日志中发现{len(error_lines)}条ERROR：\n{error_text}"

    data = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }

    try:
        response = requests.post(webhook, json=data, timeout=5)
        print("✅ 钉钉告警已发送：", response.text)
    except:
        print("❌ 钉钉发送失败，网络异常")
else:
    print("✅ 日志正常，没有ERROR")

