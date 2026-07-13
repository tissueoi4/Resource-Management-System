from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('employee_number', 'last_name', 'first_name')

class AdminEmployeeCreateForm(UserCreationForm):
    """管理者が社員アカウントを作成するための専用フォーム"""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('employee_number', 'last_name', 'first_name', 'role')