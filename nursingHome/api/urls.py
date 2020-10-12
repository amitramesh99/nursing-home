from django.urls import path
from .views import *

urlpatterns = [
    path('', CreatePatientAPIView.as_view(), name='create-patient'),
    #path('create-note', CreateNoteAPIView.as_view(), name='note-create'),
    path('notes/<int:patient>', CreateRetrieveNotesAPIView.as_view(), name='notes'),
    #path('vitals/<int:patient>', RetrieveVitalsAPIView.as_view(), name='retrieve-vitals'),
    path('activities/<int:patient>', CreateRetrieveActivitiesAPIView.as_view(), name='activities'),
    path('blood-sugar/<int:patient>', RetrieveBloodSugarView.as_view(), name='blood-sugar'),
    path('blood-pressure/<int:patient>', RetrieveBloodPressureView.as_view(), name='blood-pressure'),
    path('pulse/<int:patient>', RetrievePulseView.as_view(), name='pulse'),
    path('temp/<int:patient>', RetrieveTemperatureView.as_view(), name='temp'),
    path('weight/<int:patient>', RetrieveWeightView.as_view(), name='weight')
    #path('retrieve-patients', 'retrieve-patients')
    #path('create-patient', 'create-patient')
]
