from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.

@login_required
def home(request):
    try:
        StaffMember.objects.get(id=request.user.staffMember.id)
    except StaffMember.DoesNotExist:
        return HttpResponse("Authenticated user is not a staffMember")



    return render(request, 'dashboard/nurseDashboard.html')

# Login

# Register StaffMember
# StaffMember dashboard
# Patient: create, view, edit
# Record: create, view, edit

# Register AuthorizedViewer
# AuthorizedViewer dashboard
