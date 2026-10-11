from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction

from .models import Profile


class StudentRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=150, label='Full name')
    student_id = forms.CharField(max_length=30, label='Student ID')
    department = forms.CharField(max_length=100, required=False, label='Department')
    email = forms.EmailField(label='Email address')

    field_order = [
        'full_name', 'student_id', 'department',
        'username', 'email', 'password1', 'password2',
    ]

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def save(self, commit=True):
        with transaction.atomic():
            user = super().save(commit=False)
            user.email = self.cleaned_data['email']
            user.save()
            Profile.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                student_id=self.cleaned_data['student_id'],
                department=self.cleaned_data['department'],
            )
        return user