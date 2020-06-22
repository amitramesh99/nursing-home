from django.contrib import admin
from .models import Facility, StaffMember, Patient, AuthorizedViewer, Record

# Register your models here.

admin.site.register(Facility)
admin.site.register(StaffMember)
admin.site.register(Patient)
admin.site.register(AuthorizedViewer)
admin.site.register(Record)
