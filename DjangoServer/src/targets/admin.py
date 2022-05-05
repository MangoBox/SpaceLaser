from django.contrib import admin

# Register your models here.
from .models import DeepSpaceTarget, SolarTarget

admin.site.register(DeepSpaceTarget)
admin.site.register(SolarTarget)