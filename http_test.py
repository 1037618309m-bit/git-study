# HTTP请求练习
import requests

# 访问一个测试接口，拿到返回数据
response = requests.get("https://httpbin.org/get")

print("状态码：", response.status_code)
print("返回内容：")
print(response.text)

