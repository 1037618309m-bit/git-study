# 读取日志，自动挑出ERROR行
with open("app.log", "r") as f:
    lines = f.readlines()

error_count = 0
error_lines = []

for line in lines:
    line = line.strip()
    if "ERROR" in line:
        error_count += 1
        error_lines.append(line)

print(f"日志总行数：{len(lines)}")
print(f"发现 {error_count} 条ERROR：")
print("---")
for e in error_lines:
    print(e)

