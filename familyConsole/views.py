from django.shortcuts import render
from dashboard.models import *

# Create your views here.

def dashboard(request):
    return render(request, 'console/feed.html')

def medications(request):
    return render(request, 'console/medications.html')

def metrics(request):
    metric_models = [BloodSugarEntry, BloodPresureEntry, PulseEntry, TemperatureEntry, WeightEntry]
    daily_metrics = []
    patientId = 1
    for model in metric_models:
        try:
            daily_metrics.append(model.objects.filter(patient=patientId).latest('created_at'))
        except:
            pass

    return render(request, 'console/metrics.html', {
        'metrics': daily_metrics
    })

def activities(request):
    patient = 1
    activity_list = ActivityEntry.objects.filter(patient=patient)
    return render(request, 'console/activities.html', {
        'activity_list': activity_list
    })
