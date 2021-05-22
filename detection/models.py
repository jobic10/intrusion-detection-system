from django.db import models
from account.models import CustomUser
# Create your models here.


class Logs(models.Model):
    CATEGORY = [('L', 'Login'), ('R', 'Register')]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
    location = models.CharField(max_length=100)
    device = models.CharField(max_length=20)
    browser = models.CharField(max_length=50)
    os = models.CharField(max_length=50)
    device_family = models.CharField(max_length=50)
    category = models.CharField(max_length=1, choices=CATEGORY)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} with ip {self.ip} and OS {self.os}"


class FalseLogin(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} with status {self.seen}"
