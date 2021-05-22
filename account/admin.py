from django.contrib import admin
from .models import *  # , Course, Registration
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Course)
admin.site.register(Registration)
# admin.site.register(Course)
# admin.site.register(Registration)
