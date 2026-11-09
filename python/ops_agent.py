# 运维Agent：采集DWS报错日志 → 服务器信息 → 大模型分析 → 钉钉推送
import requests
import subprocess
import os
import time


# 钉钉机器人地址
webhook = "https://oapi.dingtalk.com/robot/send?access_token=98e33568c28c2ad62504118c4abab1cbcc83e7544dd627441a9d8c1d119c9cef"

# Ollama地址（Windows上的Ollama）
ollama_url = "http://192.168.233.1:11434/api/generate"
model_name = "it-fde-qwen3:latest"

# 第一步：读日志，挑ERROR行
print("第一步：读日志挑ERROR...")
offset_file = "/home/mino/git-study/log_offset.txt"
last_offset = 0
if os.path.exists(offset_file):
    with open(offset_file, "r") as f:
        last_offset = int(f.read().strip())

with open("/home/mino/git-study/app.log", "r") as f:
    lines = f.readlines()

new_lines = lines[last_offset:]
error_lines = []
for line in new_lines:
    line = line.strip()
    if "ERROR" in line:
        error_lines.append(line)

with open(offset_file, "w") as f:
    f.write(str(len(lines)))

error_text = "\n".join(error_lines)




print(f"发现{len(error_lines)}条ERROR：")
for e in error_lines:
    print(f"  - {e}")

# 第二步：采集服务器信息
print("\n第二步：采集服务器信息...")

# 采集磁盘使用情况
disk = subprocess.run(["df", "-h"], capture_output=True, text=True).stdout
print(f"磁盘使用情况：\n{disk}")

# 解析根分区（/）使用率
disk_used_percent = 0
for line in disk.split("\n"):
    if line.strip().endswith(" /"):
        parts = line.split()
        disk_used_percent = int(parts[4].replace("%", ""))
print(f"根分区使用率：{disk_used_percent}%")

# 精简磁盘信息：只保留根分区那一行
disk_lines = disk.split("\n")
root_line = [line for line in disk_lines if line.strip().endswith(" /")]
disk_summary = root_line[0] if root_line else "未找到根分区"



# 采集内存使用情况（顺便算出使用百分比）
memory = subprocess.run(["free", "-m"], capture_output=True, text=True).stdout
print(f"内存使用情况：\n{memory}")

mem_used_percent = 0
for line in memory.split("\n"):
    if line.strip().startswith("Mem:"):
        parts = line.split()
        mem_total = int(parts[1])
        mem_used = int(parts[2])
        mem_used_percent = int(mem_used / mem_total * 100)
print(f"内存使用率：{mem_used_percent}%")


# 采集CPU使用情况
cpu = subprocess.run(["top", "-bn1"], capture_output=True, text=True).stdout.split("\n")[2]
print(f"CPU使用情况：\n{cpu}")

# 报警条件：有ERROR 或 磁盘使用率超过85%
if len(error_lines) == 0 and disk_used_percent <= 85 and mem_used_percent <= 85:

    print(f"✅ 一切正常：无ERROR，磁盘{disk_used_percent}%低于阈值85%，内存{mem_used_percent}%低于阈值85%，不报警")

    exit()
print("⚠️ 触发告警条件，继续分析...")

# 第四步：避免重复报警（同一问题2小时内只报1次）
alert_state_file = "/home/mino/git-study/last_alert.txt"   # 记账本：记录上次报警
alert_sign = f"{error_text.replace(chr(10), ' ')}|{disk_used_percent}"  # 指纹：换行换成空格，一行到底


last_sign = ""
last_time = 0
if os.path.exists(alert_state_file):                       # 记账本存在吗？
    with open(alert_state_file, "r") as f:
        lines = f.read().split("\n")                       # 读两行：时间+指纹
        if len(lines) >= 2:
            last_time = float(lines[0])                    # 上次报警时间
            last_sign = lines[1]                           # 上次报警指纹

if last_sign == alert_sign and time.time() - last_time < 10:
    print("同一问题2小时内已报过，跳过本次报警")
    exit()



# 第三步：调用大模型分析
print("\n第三步：调用大模型分析...")

prompt = f"""你是运维告警助手。下面是DWS数据库报错日志和服务器情况，请用最短的话给出告警摘要：

【报错日志】
{error_text}

【服务器磁盘情况】
{disk}

【服务器内存情况】
内存使用率：{mem_used_percent}%


【服务器CPU情况】
{cpu}

请严格按这个格式输出，不超过5行：
【问题】一句话说明
【原因】一句话说明
【建议】一句话说明（给1条最优先的命令）
"""


data = {
    "model": model_name,
    "prompt": prompt,
    "stream": False,
    "think": False,
    "keep_alive": -1,


    "options": {
        "num_predict": 120
    }
}

response = requests.post(ollama_url, json=data, timeout=120)
result = response.json()
ai_answer = result["response"]


# 去掉<think>标签和思考过程（不管有没有</think>都能去掉）
ai_answer = ai_answer.replace("<think>", "").replace("</think>", "")



print(f"大模型分析结果：\n{ai_answer}")





# 第五步：发钉钉
print("\n第四步：发钉钉告警...")

content = f"""🚨 运维告警

📋 报错日志：
{error_text}

📊 服务器磁盘：
{disk_summary}

💾 服务器内存：
内存使用率 {mem_used_percent}%

📈 服务器CPU：
{cpu}

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

# 记录本次报警（写进记账本）
with open(alert_state_file, "w") as f:
    f.write(f"{time.time()}\n{alert_sign}")

