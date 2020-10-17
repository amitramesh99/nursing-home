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
            'patient',
            'notes',
            'category',
            'severity',
            'created_at'
        ]

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityEntry
        fields = [
            'patient',
            'name',
            'description',
            'intensity',
            'created_at'
        ]

class BloodSugarSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodSugarEntry
        fields = [
            'LABEL',
            'entry',
            'UNIT',
            'created_at'
        ]

class BloodPressureSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodPressureEntry
        fields = [
            'LABEL',
            'entry',
            'UNIT',
            'created_at'
        ]

class PulseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PulseEntry
        fields = [
            'LABEL',
            'entry',
            'UNIT',
            'created_at'
        ]

class TemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperatureEntry
        fields = [
            'LABEL',
            'entry',
            'UNIT',
            'created_at'
        ]

class WeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightEntry
        fields = [
            'LABEL',
            'entry',
            'UNIT',
            'created_at'
        ]
