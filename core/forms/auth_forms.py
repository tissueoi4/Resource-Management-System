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

class ProfileEditForm(forms.ModelForm):
    """ユーザーが自分自身のプロフィールを編集するためのフォーム"""
    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'email')
        labels = {
            'last_name': '姓 (本名)',
            'first_name': '名 (本名)',
            'email': 'メールアドレス',
        }
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: 田中'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: 太郎'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '例: taro@example.com'}),
        }