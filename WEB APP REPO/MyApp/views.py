from django.shortcuts import render
from .models import TodoItem

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Task
from datetime import timedelta

def home(request):
    return render(request, "home.html")

def todos(request):
    items = TodoItem.objects.all()
    return render(request, "todos.html", {"todos":items})

#---------------------------------------------------------------

def calendar_view(request):
    return render(request, "calendar.html")

def task_events(request):
    tasks = Task.objects.filter(user=request.user)
    events = []
    for task in tasks:
        if task.is_snoozed and task.snoozed_until and task.snoozed_until > timezone.now():
            continue  # skip snoozed tasks
        events.append({
            "id": task.id,
            "title": task.title,
            "start": task.start_time.isoformat(),
            "end": task.end_time.isoformat(),
        })
    return JsonResponse(events, safe=False)


@csrf_exempt
def create_task(request):
    global task
    if request.method == "POST":
        data = request.POST
        task = Task.objects.create(
            user=request.user,
            title=data["title"],
            start_time=data["start"],
            end_time=data["end"],
            reminder_time=data.get("reminder")
        )
        return JsonResponse({"status": "created"})

@csrf_exempt
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return JsonResponse({"status": "deleted"})

@csrf_exempt
def snooze_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_snoozed = True
    task.snoozed_until = timezone.now() + timedelta(hours=1)
    task.save()
    return JsonResponse({"status": "snoozed"})
