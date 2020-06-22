from django.db import models
from django.contrib.auth.models import User

class Facility(models.Model):
    name = models.CharField(max_length=200)
    # location

class StaffMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="staffMembers")


class Patient(models.Model):
    name = models.CharField(max_length=50)
    # primary contact?


class AuthorizedViewer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # email
    # phone number
    patients = models.ManyToManyField(Patient)


class Records(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="records")
    time_recorded = models.DateTimeField(auto_now=True)

    # Vitals:
    # weight
    # BP
    # etc

    # Wellness:
    # mood?

    # Activities:
    # message? -> seperate model w/ picture?
