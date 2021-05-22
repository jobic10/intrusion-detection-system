from django.contrib import admin
from .models import Logs, FalseLogin
# Register your models here.
admin.site.register(Logs)
admin.site.register(FalseLogin)
