# 定义一个告警判断函数
def check_mem(mem_value):
    if mem_value >=70:
        return "⚠️ 内存超标告警"
    else:
        return "✅ 内存正常"


server_list = [
    {"ip":"192.168.1.10", "mem":60},
    {"ip":"192.168.1.11", "mem":85},
    {"ip":"192.168.1.12", "mem":40}
]

for server in server_list:
    ip = server["ip"]
    mem = server["mem"]
    res = check_mem(mem)
    print(f"【{ip}】内存：{mem}%，结果：{res}")

