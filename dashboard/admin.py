from django.contrib import admin
from .models import Facility, StaffMember, Patient, AuthorizedViewer, Records

# Register your models here.

admin.site.register(Facility)
admin.site.register(StaffMember)
admin.site.register(Patient)
admin.site.register(AuthorizedViewer)
admin.site.register(Records)
