# 文件读写练习
# 第一步：往文件里写内容
with open("server_log.txt", "w") as f:
    f.write("2026-10-27 服务器启动成功\n")
    f.write("2026-10-27 内存使用率60%，正常\n")
    f.write("2026-10-27 磁盘使用率45%，正常\n")

# 第二步：把文件内容读出来
with open("server_log.txt", "r") as f:
    content = f.read()

print("===== 读出来的日志内容 =====")
print(content)

