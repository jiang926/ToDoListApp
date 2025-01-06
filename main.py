from datetime import date
from pydantic import BaseModel
from typing import Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import database


app = FastAPI(title="To-Do list App", version="1.0.0")
# 设置模板目录
templates = Jinja2Templates(directory="templates")


class Task(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    priority: Optional[int] = 3


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    tasks = database.read_task_all_data()
    # 渲染模板并传递上下文数据
    return templates.TemplateResponse("index.html", {"request": request, "title": "FastAPI Example", "tasks": tasks})


@app.post("/tasks/create")
async def create_task(task: Task):
    """
    创建任务
    :param task:
    :return:
    """
    database.write_task_to_data(task)
    return {"message": "任务创建成功", "task": task}


@app.put("/tasks/{task_id}/edit")
async def update_task(task_id: int, up_data_task: Task):
    try:
        database.update_task_data(task_id, up_data_task)
    except Exception as e:
        return {"message": "任务更新失败", "error": e}
    return {"message": "任务更新成功", "up_data_task": up_data_task}


@app.delete("/tasks/{task_id}/delete")
async def delete_task(task_id: int):
    database.delete_task_data_by_id(task_id)
    return {"message": "任务删除成功"}
