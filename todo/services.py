from django.http import QueryDict
from distutils.util import strtobool
from django.contrib.auth.models import User

from .models import Task


def delete_task(request_body: bytes) -> None:
    """Takes pk from given request body and deletes task
       with this pk or raises Does Not Exist Error"""
    pk = QueryDict(request_body)['pk']
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist as e:
        raise e
    else:
        task.delete()


def create_task(request_body: bytes, user: User) -> None:
    """Takes text for new task from request body and creates
       new task with it and given user"""
    task_text = QueryDict(request_body)['text']
    new_task = Task(text=task_text, user=user)
    new_task.save()


def update_task(request_body: bytes) -> None:
    """Takes pk and status from request body,
       changes is_completed field to status to task with pk=pk
       or raises Does Not Exist Error"""
    request_params = QueryDict(request_body)
    pk = request_params['pk']
    status = strtobool(request_params['completed'])
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist as e:
        raise e
    else:
        task.is_completed = status
        task.save()


def get_completed_or_uncompleted_tasks_by_user(user: User, is_completed: bool) -> QueryDict:
    """Returns all tasks with given status and created by given user"""
    return Task.objects.filter(is_completed=is_completed).filter(user=user)
