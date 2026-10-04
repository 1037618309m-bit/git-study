# 调用Linux系统命令
import subprocess

# 执行 free -h，查看真实内存
result = subprocess.run(["free", "-h"], capture_output=True, text=True)

print("===== 服务器真实内存 =====")
print(result.stdout)

# 再执行 df -h，查看磁盘
result2 = subprocess.run(["df", "-h"], capture_output=True, text=True)
print("===== 服务器真实磁盘 =====")
print(result2.stdout)
