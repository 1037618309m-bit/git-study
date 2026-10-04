# 按行读日志 + 关键词筛选
with open("server_log.txt", "r") as f:
    lines = f.readlines()

print(f"日志一共有 {len(lines)} 行")
print("===== 开始逐行筛选 =====")

for line in lines:
    line = line.strip()

    if "内存" in line:
        print(f"[内存类] {line}")
    elif "磁盘" in line:
        print(f"[磁盘类] {line}")
    else:
        print(f"[其他] {line}")

