# 完整实战：自动巡检内存 + 钉钉告警
import subprocess
import requests

# 钉钉机器人地址
webhook = "https://oapi.dingtalk.com/robot/send?access_token=98e33568c28c2ad62504118c4abab1cbcc83e7544dd627441a9d8c1d119c9cef"

# 第一步：执行free命令，拿真实内存数据
result = subprocess.run(["free"], capture_output=True, text=True)
lines = result.stdout.split("\n")
mem_line = lines[1]
parts = mem_line.split()

total_mem = int(parts[1])
used_mem = int(parts[2])
usage = used_mem / total_mem * 100

print(f"当前内存使用率：{usage:.1f}%")

# 第二步：判断是否超标
if usage >= 50:
    print("⚠️ 内存超标，发送钉钉告警！")

    # 第三步：发钉钉消息
    data = {
        "msgtype": "text",
        "text": {
            "content": f"告警：服务器内存使用率{usage:.1f}%，超过50%阈值！请尽快处理。"
        }
    }
    response = requests.post(webhook, json=data)
    print("钉钉返回：", response.text)
else:
    print("✅ 内存正常，不需要告警")

