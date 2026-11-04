# 实战：自动读取真实内存并判断告警
import subprocess

# 执行free命令，拿到输出
result = subprocess.run(["free"], capture_output=True, text=True)

# 把输出按行切开
lines = result.stdout.split("\n")

# 第二行是Mem那一行
mem_line = lines[1]

# 按空格切开，取出每一列数字
parts = mem_line.split()

total_mem = int(parts[1])   # 总内存
used_mem = int(parts[2])   # 已用内存

# 算使用率
usage = used_mem / total_mem * 100

# 字节转成MB，好看一点
total_mb = total_mem / 1024
used_mb = used_mem / 1024

print(f"总内存：{total_mb:.1f} MB")
print(f"已用内存：{used_mb:.1f} MB")
print(f"内存使用率：{usage:.1f}%")

if usage >= 70:
    print("⚠️ 内存使用率超过70%，触发告警！")
else:
    print("✅ 内存正常")

