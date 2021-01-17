from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from . import services


@never_cache
@login_required(login_url='login')
def todo_list(request):
    if request.method.lower() == 'delete':
        services.delete_task(request.body)
    elif request.method.lower() == 'post':
        services.create_task(request.body, request.user)
    elif request.method.lower() == 'put':
        services.update_task(request.body)
    completed_tasks = services.get_completed_or_uncompleted_tasks_by_user(
        user=request.user,
        is_completed=True
    )
    uncompleted_tasks = services.get_completed_or_uncompleted_tasks_by_user(
        user=request.user,
        is_completed=False
    )
    context = {'completed_tasks': completed_tasks,
               'uncompleted_tasks': uncompleted_tasks
               }
    return render(request, 'todo/list.html', context)


def home(request):
    return render(request, 'todo/home.html')