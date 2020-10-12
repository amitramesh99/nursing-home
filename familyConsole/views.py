from django.shortcuts import render, HttpResponse
from dashboard.models import *
import json

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

def communication(request):
    try:
        # TODO: Handle case of multiple patients
        patient = request.user.authorizedViewer.patients.first()
        patientId = patient.id
        patient_json = json.dumps(patient.as_dict())
    except Patient.DoesNotExist:
        patient = None
        patientId = None
        patient_json = ''

    return render(request, 'console/communication.html', {
        'patient_json': patient_json,
        'chat_id': f'patient-{patientId}',

    })

def vital_hub(request):
    metric_models = [BloodSugarEntry, BloodPressureEntry, PulseEntry, TemperatureEntry, WeightEntry]
    daily_metrics = []
    patientId = 1
    for model in metric_models:
        try:
            daily_metrics.append(model.objects.filter(patient=patientId).latest('created_at'))
        except:
            pass

    current_prescriptions = Medication.objects.filter(patient=patientId)
    activity_list = ActivityEntry.objects.filter(patient=patientId)

    return render(request, 'console/vital_hub.html', {
        'metrics': daily_metrics,
        'current_prescriptions': current_prescriptions,
        'activity_list': activity_list
    })

def wellbeing(request):
    patient = 1
    activity_list = ActivityEntry.objects.filter(patient=patient)
    return render(request, 'console/wellbeing.html', {
        'activity_list': activity_list
    })

def chat(request):
    return HttpResponse("Family chat view goes here")
