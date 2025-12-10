from fastapi import APIRouter 
from schema.task import Task
from fixture import tasks as fixture_task
from database import get_db_connection

router = APIRouter(prefix="/task", tags = ["task"])


@router.get("/all",
    response_model = list[Task])
async def get_tasks():
    cursor = get_db_connection().cursor()
    tasks = cursor.execute("SELECT * FROM Tasks").fetchall()
    print(tasks)
    return fixture_task


@router.post(
    "/",
    response_model=Task)
async def create_task(task: Task):
    fixture_task.append(task)
    return task


@router.patch("/{task_id}")
async def patch_task(task_id: int, name: str):
    for task in fixture_task:
        if task['id'] == task_id:
            task['name'] = name
    return {"message": f'task with {task_id} have name {name}'}


@router.delete("/{task_id}")
async def delete_task(task_id: int):
    for i, task in enumerate(fixture_task):
        if task['id'] == task_id:
            del fixture_task[i]
            return {"message": f'task {task_id} is delete'}
    return {'message': 'нет такого id'}
