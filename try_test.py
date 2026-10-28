# 异常处理练习
import requests

# 故意发一个会超时的请求
# delay/10 意思是服务器延迟10秒才响应
# timeout=2 意思是我们只等2秒，超时就放弃
try:
    response = requests.get("https://httpbin.org/delay/10", timeout=2)
    print("请求成功！状态码：", response.status_code)
except requests.exceptions.Timeout:
    print("⏰ 请求超时了！服务器没响应")
except requests.exceptions.ConnectionError:
    print("📡 网络不通！连接失败")

