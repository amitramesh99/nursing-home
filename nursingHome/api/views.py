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

    def post(self, request, *args, **kwargs):
        _mutable = request.data._mutable
        request.data._mutable = True
        request.data['patient'] = self.kwargs['patient']
        _mutable = False
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        return NoteEntry.objects.filter(patient=self.kwargs['patient'])

class CreateRetrieveActivitiesAPIView(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer

    def post(self, request, *args, **kwargs):
        _mutable = request.data._mutable
        request.data._mutable = True
        request.data['patient'] = self.kwargs['patient']
        _mutable = False
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        return ActivityEntry.objects.filter(patient=self.kwargs['patient'])
