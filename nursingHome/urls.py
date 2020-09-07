"""nursingHome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

from dashboard import views as dashboard_views
from familyConsole import views as family_views

from nursingHome.api import views as api_views

urlpatterns = [
    # django urls
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', dashboard_views.home, name='home'),

    path('token/chat', dashboard_views.get_chat_token, name='chat-token'),
    path('token/video', dashboard_views.get_video_token, name='video-token'),

    path('video/', dashboard_views.video_conference, name='video'),

    # nurse view
    path('dashboard/', dashboard_views.nurse_dashboard, name='nurse-dashboard'),
    path('dashboard/patient/<int:patientId>/', dashboard_views.patient_profile, name='profile'),
    path('dashboard/patient/<int:patientId>/chat', dashboard_views.patient_chat, name='patient-chat'),

    # family view
    path('portal/', family_views.dashboard, name='family-dashboard'),
    path('portal/vitals', family_views.vital_hub, name='vital_hub'),
    path('portal/wellbeing', family_views.wellbeing, name='wellbeing'),
    path('portal/medications/', family_views.medications, name='medications'),
    path('portal/metrics/', family_views.metrics, name='metrics'),
    path('portal/activities/', family_views.activities, name='activities'),
    path('portal/chat/', family_views.chat, name='family-chat'),

    path('api/patients/', include(('nursingHome.api.urls', 'nursingHome'), namespace='api-patients'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
