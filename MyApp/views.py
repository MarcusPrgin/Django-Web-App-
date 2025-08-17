from django.shortcuts import render
from .models import TodoItem

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Task
from datetime import timedelta

from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Marker
import json

def map_view(request):
    markers = Marker.objects.all().values('id', 'latitude', 'longitude')
    return render(request, 'map.html', {
        'markers': list(markers),
    })

@csrf_exempt
def add_marker(request):
    if request.method == "POST":
        data = json.loads(request.body)
        lat = data.get("latitude")
        lng = data.get("longitude")
        marker = Marker.objects.create(latitude=lat, longitude=lng)
        return JsonResponse({"id": marker.id})

@csrf_exempt
def delete_marker(request, marker_id):
    try:
        marker = Marker.objects.get(id=marker_id)
        marker.delete()
        return JsonResponse({"status": "deleted"})
    except Marker.DoesNotExist:
        return JsonResponse({"error": "not found"}, status=404)

@csrf_exempt
def clear_markers(request):
    if request.method == "DELETE":
        Marker.objects.all().delete()
        return JsonResponse({"status": "cleared"})


def map_view(request):
    return render(request, 'map.html')


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
