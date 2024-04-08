"""
URL configuration for smartcare_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from knox import views as knox_views

from smartcare_auth.views import UserView, StaffView, LoginView
from smartcare_appointments.views import AppointmentView, TimeOffView, PrescriptionsView
from smartcare_finance.views import InvoiceView, generate_turnover_report

router = routers.DefaultRouter()
router.register(r"auth/user", UserView, basename="user")
router.register(r"appointments", AppointmentView, basename="appointment")
router.register(r"staff", StaffView, basename="staff")
router.register(r'timeoff', TimeOffView)
router.register(f"invoice", InvoiceView, basename="invoice")
router.register(r"prescriptions", PrescriptionsView)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
# TODO: Being able to log in via the drf frontend should only really be possible in DEBUG, remove or make this conditional on that setting!!!
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/auth/login/", LoginView.as_view(), name="knox_login"),
    path("api/auth/logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    path("api/auth/logoutall/", knox_views.LogoutAllView.as_view(), name="knox_logoutall"),
    path("api/generate-turnover-report/", generate_turnover_report),
# Following only works in development, django will not serve these files in production
# https://docs.djangoproject.com/en/5.0/howto/static-files/#serving-files-uploaded-by-a-user-during-development
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls