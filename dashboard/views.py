from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *

# Create your views here.

def is_nurse(user):
    return hasattr(user, 'staffMember')

@user_passes_test(is_nurse)
def home(request):
    facility = StaffMember.objects.get(id=request.user.staffMember.id).facility

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


    return render(request, 'dashboard/patient_profile.html', {
        'facility': facility,
        'patient_list': patient_list,
        'patient': patient,
    })
