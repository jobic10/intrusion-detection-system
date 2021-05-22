from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'
        for fieldname in ['password1', 'password2', 'username']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']
