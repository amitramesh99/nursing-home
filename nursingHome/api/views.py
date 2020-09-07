from dashboard.models import Patient
from rest_framework import generics
from rest_framework.response import Response
from .serializers import *

from rest_framework.decorators import api_view

'''
@api_view(['GET'])
def retrieve_patients(request):
    patients = Patient.objects.all()
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_patient(request):

'''

class CreatePatientAPIView(generics.CreateAPIView):
    #lookup_field = 'pk'
    serializer_class = PatientSerializer

    #def get_queryset(self):
    #    return Patient.objects.all()

#class CreateNoteAPIView(generics.CreateAPIView):
    #lookup_field = 'pk'
#    serializer_class = NoteSerializer

    #def get_queryset(self):
    #    return NoteEntry.objects.all()

class CreateRetrieveNotesAPIView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer

    def get_queryset(self):
        return NoteEntry.objects.filter(patient=self.kwargs['patient'])

class CreateRetrieveActivitiesAPIView(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer

    def get_queryset(self):
        return ActivityEntry.objects.filter(patient=self.kwargs['patient'])


#class PatientInfoRetrieveAPIView(generics.RetrieveAPIView):
#    lookup_field = 'pk'


    #def perform_create(self, serializer):
    #    serializer.save(user=self.request.user)
