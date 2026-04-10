from app.services.task_service import add_task as service_add_task, list_tasks as service_list_tasks


def add_task(task: str):
    return service_add_task(task)


def get_tasks():
    return service_list_tasks()
