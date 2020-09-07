from django.shortcuts import render, HttpResponse
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

def vital_hub(request):
    metric_models = [BloodSugarEntry, BloodPresureEntry, PulseEntry, TemperatureEntry, WeightEntry]
    daily_metrics = []
    patientId = 1
    for model in metric_models:
        try:
            daily_metrics.append(model.objects.filter(patient=patientId).latest('created_at'))
        except:
            pass

    current_prescriptions = Medication.objects.filter(patient=patientId)

    return render(request, 'console/vital_hub.html', {
        'metrics': daily_metrics,
        'current_prescriptions': current_prescriptions
    })

def wellbeing(request):
    patient = 1
    activity_list = ActivityEntry.objects.filter(patient=patient)
    return render(request, 'console/wellbeing.html', {
        'activity_list': activity_list
    })

def chat(request):
    return HttpResponse("Family chat view goes here")
