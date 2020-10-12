from dashboard.models import *
from rest_framework import generics
from rest_framework.response import Response
from .serializers import *

from rest_framework.decorators import api_view

class CreatePatientAPIView(generics.CreateAPIView):
    serializer_class = PatientSerializer

    def post(self, request, *args, **kwargs):
        _mutable = request.data._mutable
        request.data._mutable = True
        facility = StaffMember.objects.get(id=request.user.staffMember.id).facility.id
        request.data.update({"facility": facility})
        _mutable = False
        return self.create(request, *args, **kwargs)

    #def get_queryset(self):
    #    return Patient.objects.all()

class CreateRetrieveNotesAPIView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer

    #def post(self, request, *args, **kwargs):
    #    print('reached')
    #    _mutable = request.data._mutable
    #    request.data._mutable = True
    #    request.data['patient'] = self.kwargs['patient']
    #    _mutable = False
    #    return self.create(request, *args, **kwargs)

    def get_queryset(self):
        return reversed(NoteEntry.objects.filter(patient=self.kwargs['patient']).order_by('-created_at')[:3])

class CreateRetrieveActivitiesAPIView(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer

    '''
    def post(self, request, *args, **kwargs):
        _mutable = request.data._mutable
        request.data._mutable = True
        request.data['patient'] = self.kwargs['patient']
        _mutable = False
        return self.create(request, *args, **kwargs)
    '''

    def get_queryset(self):
        # Returns 3 most recent activities
        return reversed(ActivityEntry.objects.filter(patient=self.kwargs['patient']).order_by('-created_at')[:3])

class RetrieveBloodSugarView(generics.RetrieveAPIView):
    serializer_class = BloodSugarSerializer
    lookup_field = 'patient'

    def get_object(self):
        return BloodSugarEntry.objects.filter(patient=self.kwargs['patient']).latest('created_at')

class RetrieveBloodPressureView(generics.RetrieveAPIView):
    serializer_class = BloodPressureSerializer
    lookup_field = 'patient'

    def get_object(self):
        return BloodPressureEntry.objects.filter(patient=self.kwargs['patient']).latest('created_at')

class RetrieveBloodSugarView(generics.RetrieveAPIView):
    serializer_class = BloodSugarSerializer
    lookup_field = 'patient'

    def get_object(self):
        return BloodSugarEntry.objects.filter(patient=self.kwargs['patient']).latest('created_at')

class RetrievePulseView(generics.RetrieveAPIView):
    serializer_class = PulseSerializer
    lookup_field = 'patient'

    def get_object(self):
        return PulseEntry.objects.filter(patient=self.kwargs['patient']).latest('created_at')

class RetrieveTemperatureView(generics.RetrieveAPIView):
    serializer_class = TemperatureSerializer
    lookup_field = 'patient'

    def get_object(self):
        return TemperatureEntry.objects.filter(patient=self.kwargs['patient']).latest('created_at')

class RetrieveWeightView(generics.RetrieveAPIView):
    serializer_class = WeightSerializer
    lookup_field = 'patient'

    def get_object(self):
        return WeightEntry.objects.filter(patient=self.kwargs['patient']).latest('created_at')
