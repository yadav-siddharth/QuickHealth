from django.contrib import admin

from app.models import Patient
from app.models import Doctor
from app.models import Appointment
from .models import *

# Register your models here.

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
