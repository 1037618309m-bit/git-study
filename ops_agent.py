# 运维Agent：采集DWS报错日志 → 大模型分析 → 钉钉推送
import requests

# 钉钉机器人地址
webhook = "https://oapi.dingtalk.com/robot/send?access_token=98e33568c28c2ad62504118c4abab1cbcc83e7544dd627441a9d8c1d119c9cef"

# Ollama地址（Windows上的Ollama）
ollama_url = "http://192.168.233.1:11434/api/generate"
model_name = "it-fde-qwen3:latest"

# 第一步：读日志，挑ERROR行
print("第一步：读日志挑ERROR...")
with open("app.log", "r") as f:
    lines = f.readlines()

error_lines = []
for line in lines:
    line = line.strip()
    if "ERROR" in line:
        error_lines.append(line)

if len(error_lines) == 0:
    print("✅ 日志正常，没有ERROR")
    exit()

print(f"发现{len(error_lines)}条ERROR：")
for e in error_lines:
    print(f"  - {e}")

# 第二步：调用大模型分析日志
# print("\n第二步：调用大模型分析...")
error_text = "\n".join(error_lines)

# prompt = f"""你是一个运维专家。下面是DWS数据库的报错日志，请分析原因并给出解决方案：

# {error_text}

# 请用大白话回答：
# 1. 报错原因是什么？
# 2. 怎么解决？
# """

# data = {
#     "model": model_name,
#     "prompt": prompt,
#     "stream": False
# }

# response = requests.post(ollama_url, json=data, timeout=60)
# result = response.json()
# ai_answer = result["response"]

# print(f"大模型分析结果：\n{ai_answer}")
ai_answer = "大模型分析暂时跳过，以后再加"

# 第三步：发钉钉
print("\n第三步：发钉钉告警...")
content = f"""🚨 运维告警

📋 报错日志：
{error_text}

🤖 大模型分析：
{ai_answer}
"""

data = {
    "msgtype": "text",
    "text": {
        "content": content
    }
}

response = requests.post(webhook, json=data, timeout=5)
print("钉钉返回：", response.text)

