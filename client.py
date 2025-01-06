import requests
from datetime import date

# 定义 FastAPI 服务的 URL
BASE_URL = "http://192.168.0.104:8000"  # 假设你的服务运行在本地的 8000 端口
ENDPOINT = "/tasks"  # 创建任务的路由
URL = BASE_URL + ENDPOINT

# 定义任务数据
task_data = {
    "title": "任务三",  # 任务标题
    "description": "编写开发代码",  # 任务描述
    "due_date": date.today().isoformat(),  # 截止日期（格式为 ISO 8601，例如：2025-01-04）
    "priority": 1  # 优先级（1 表示高优先级）
}

# 发送 POST 请求
response = requests.post(URL, json=task_data)

# 检查响应结果
if response.status_code == 200:
    print("任务创建成功！")
    print("返回数据：", response.json())
else:
    print(f"请求失败，状态码：{response.status_code}")
    print("错误信息：", response.text)
