from rest_framework import serializers
from dashboard.models import *

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'pk',
            'name',
            'facility'
        ]

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteEntry
        fields = [
            'pk',
            'patient',
            'notes',
            'category',
            'severity'
        ]

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityEntry
        fields = [
            'pk',
            'patient',
            'name',
            'description',
            'intensity'
        ]
