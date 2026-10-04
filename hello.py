# for + if 组合巡检
server_list = [
    {"ip":"192.168.1.10", "mem":60},
    {"ip":"192.168.1.11", "mem":85},
    {"ip":"192.168.1.12", "mem":40}
]

for server in server_list:
    ip = server["ip"]
    mem = server["mem"]
    print(f"正在检查 {ip}，内存使用率：{mem}%")

    if mem >= 70:
        print(f"⚠️ {ip} 内存超标，触发告警！")
    else:
        print(f"✅ {ip} 内存正常")
