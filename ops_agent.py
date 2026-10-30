# 运维Agent：采集DWS报错日志 → 服务器信息 → 大模型分析 → 钉钉推送
import requests
import subprocess

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

# 第二步：采集服务器信息
print("\n第二步：采集服务器信息...")

# 采集磁盘使用情况
disk = subprocess.run(["df", "-h"], capture_output=True, text=True).stdout
print(f"磁盘使用情况：\n{disk}")

# 采集内存使用情况
memory = subprocess.run(["free", "-h"], capture_output=True, text=True).stdout
print(f"内存使用情况：\n{memory}")

# 第三步：调用大模型分析
print("\n第三步：调用大模型分析...")

error_text = "\n".join(error_lines)

prompt = f"""你是一个运维专家。下面是DWS数据库的报错日志和服务器实际情况，请分析原因并给出具体解决方案：

【报错日志】
{error_text}

【服务器磁盘情况】
{disk}

【服务器内存情况】
{memory}

请用大白话回答：
1. 报错原因是什么？
2. 具体怎么解决？（给出具体命令）
"""

data = {
    "model": model_name,
    "prompt": prompt,
    "stream": False,
    "options": {
        "num_predict": 300
    }
}

response = requests.post(ollama_url, json=data, timeout=120)
result = response.json()
ai_answer = result["response"]

print(f"大模型分析结果：\n{ai_answer}")

# 第四步：发钉钉
print("\n第四步：发钉钉告警...")

content = f"""🚨 运维告警

📋 报错日志：
{error_text}

📊 服务器磁盘：
{disk}

🧠 大模型分析：
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
