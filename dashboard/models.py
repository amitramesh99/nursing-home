from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# User and Auth models:
class Facility(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class StaffMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staffMember')
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="staffMembers")

    def __str__(self):
        return self.user.username


class Patient(models.Model):
    name = models.CharField(max_length=50)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="patients")

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "profile_url": reverse('profile', args=[self.id]),
            "facility": self.facility.id
        }

class AuthorizedViewer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='authorizedViewer')
    # email
    # phone number
    patients = models.ManyToManyField(Patient)

    def __str__(self):
        return self.user.username


# Daily Metric models:
class MetricEntry(models.Model):
    LABEL = ''
    UNIT = ''

    created_at = models.DateTimeField(auto_now=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='%(class)s')
    entry = models.SmallIntegerField()

    class Meta:
        abstract = True
        get_latest_by = 'time_created'

    @property
    def unit(self):
        return self.UNIT

    def __str__(self):
        return "%s %s" % (str(self.entry), self.UNIT)


class BloodSugarEntry(MetricEntry):
    LABEL = 'Blood Sugar'
    UNIT = 'mg/dL'

class BloodPresureEntry(MetricEntry):
    LABEL = 'Blood Pressure'
    UNIT = 'mm Hg'

    systolic = models.SmallIntegerField()
    diastolic = models.SmallIntegerField()

    @property
    def entry(self):
        return "%d/%d" % (self.systolic, self.diastolic)

class PulseEntry(MetricEntry):
    LABEL = 'Pulse'
    UNIT = 'bpm'

class TemperatureEntry(MetricEntry):
    LABEL = 'Body Temperature'
    UNIT = '˚F'

    entry = models.FloatField()


class WeightEntry(MetricEntry):
    LABEL = 'Weight'
    UNIT = 'lb'

class SkinAssesmentEntry(MetricEntry):
    LABEL = 'Skin Assesment'

    entry = models.TextField()



# Other entry models:
class ActivityEntry(MetricEntry):
    LEVEL_OPTIONS = [
        ('l', "Light"),
        ('m', 'Moderate'),
        ('a', 'Active')
    ]

    intensity = models.CharField(
        max_length=1,
        choices=LEVEL_OPTIONS,
        default='m')

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, default='')

    @property
    def entry(self):
        return "[%s] %s: %s" % (self.get_intensity_display(), self.name, self.description)

class GeneralNoteEntry(MetricEntry):
    entry = models.TextField()

class DailyActivityOption(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class DailyActivitiesEntry(MetricEntry):
    entry = None
    activities = models.ManyToManyField(DailyActivityOption, related_name='selected_activities')

    def __str__(self):
        return str(self.activities.all())

class Day(models.Model):
    name = models.CharField(max_length=9)

    def __str__(self):
        return self.name

class Medication(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medications')

    name = models.CharField(max_length=30)
    dosage = models.CharField(max_length=20)
    notes = models.TextField(blank=True, default='')
    active = models.BooleanField(default=True)
    days = models.ManyToManyField(Day, related_name='days')

    def __str__(self):
        return "%s (%s)" % (self.name, self.dosage)

class MedicationEntry(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medication_entries')
    medications = models.ManyToManyField(Medication, related_name='selected_medications')

    def __str__(self):
        return str(self.medications.all())

# Lab Work
class LabWork(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_work_set')
    notes = models.TextField(blank=True, default='')

class UserUploadedDocument(models.Model):
    lab_work = models.ForeignKey(LabWork, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.document.name

class NoteEntry(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='%(class)s')

    notes = models.TextField(blank=True, default='')
    category = models.CharField(max_length=10)
    severity = models.CharField(max_length=10)

    def __str__(self):
        return "[%s] %s: %s" % (self.severity, self.patient, self.category)
