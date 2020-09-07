from django.urls import path
from .views import *

urlpatterns = [
    path('', CreatePatientAPIView.as_view(), name='create-patient'),
    #path('create-note', CreateNoteAPIView.as_view(), name='note-create'),
    path('notes/<int:patient>', CreateRetrieveNotesAPIView.as_view(), name='notes'),
    #path('vitals/<int:patient>', RetrieveVitalsAPIView.as_view(), name='retrieve-vitals'),
    path('activities/<int:patient>', CreateRetrieveActivitiesAPIView.as_view(), name='activities')
    #path('retrieve-patients', 'retrieve-patients')
    #path('create-patient', 'create-patient')
]
