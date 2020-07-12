from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *

# Create your views here.

def is_nurse(user):
    return hasattr(user, 'staffMember')

@user_passes_test(is_nurse)
def home(request):
    facility = StaffMember.objects.get(id=request.user.staffMember.id).facility

    if request.method == 'POST':
        name = request.POST.get('your_name')
        patient = Patient(name=name, facility=facility)
        patient.save()

    search_query = request.GET.get('q', '')
    patient_list = Patient.objects.filter(name__contains=search_query, facility=facility.id)

    return render(request, 'dashboard/nurse_dashboard.html', {
        'facility': facility,
        'patient_list': patient_list,
        'search_query': search_query
    })

@user_passes_test(is_nurse)
def patient_profile(request, patientId):
    nurse = StaffMember.objects.get(id=request.user.staffMember.id)

    try:
        patient = Patient.objects.get(id=patientId)
    except Patient.DoesNotExist:
        patient = None

    facility = nurse.facility

    search_query = request.GET.get('q', '')
    patient_list = Patient.objects.filter(name__contains=search_query)

    activity_list = ActivityEntry.objects.filter(patient=patient)
    daily_living_list = DailyActivityOption.objects.all()
    medications = Medication.objects.filter(patient=patient)


    metric_models = [BloodSugarEntry, BloodPresureEntry, PulseEntry, TemperatureEntry, WeightEntry]

    daily_metrics = []
    for model in metric_models:
        try:
            daily_metrics.append(model.objects.filter(patient=patientId).latest('created_at'))
        except:
            pass


    return render(request, 'dashboard/patient_profile.html', {
        'facility': facility,
        'patient_list': patient_list,
        'patient': patient,
        'activity_list': activity_list,
        'daily_living_list': daily_living_list,
        'medications': medications,
        'metrics': daily_metrics
    })
