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
    if request.method == 'POST':
        medication_entries = request.POST.getlist('medications')

        try:
            m = MedicationEntry.objects.get(patient_id=patientId)
            m.medications.clear()
        except:
            m = MedicationEntry(patient_id=patientId)
            m.save()

        for entry in medication_entries:
            med = Medication.objects.get(id=entry)
            m.medications.add(med)

        living_entries = request.POST.getlist('living')

        try:
            e = DailyActivitiesEntry.objects.get(patient_id=patientId)
            e.activities.clear()
        except:
            e = DailyActivitiesEntry(patient_id=patientId)
            e.save()

        for entry in living_entries:
            option = DailyActivityOption.objects.get(id=entry)
            e.activities.add(option)


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

    try:
        daily_living_completed = set(DailyActivitiesEntry.objects.filter(patient=patientId).values_list('activities', flat=True))
    except:
        daily_living_completed = []

    medications = Medication.objects.filter(patient=patient)
    try:
        medications_taken = set(MedicationEntry.objects.filter(patient=patientId).values_list('medications', flat=True))
    except:
        medications_taken = []

    return render(request, 'dashboard/patient_profile.html', {
        'facility': facility,
        'patient_list': patient_list,
        'patient': patient,
        'activity_list': activity_list,
        'daily_living_list': daily_living_list,
        'daily_living_completed': daily_living_completed,
        'medications': medications,
        'medications_taken': medications_taken
    })
