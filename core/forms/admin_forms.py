from django import forms
from django.contrib.auth import get_user_model
from core.models import Project
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class EmployeeRoleForm(forms.ModelForm):
    class Meta:
        model = User
        # モデルに定義されている role フィールド（または is_staff など）を指定
        fields = ('role',) 
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'}),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        # モデルの定義に合わせて、required_hours を追加
        fields = ('name', 'description', 'required_hours') 
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'プロジェクト名を入力'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,
                'placeholder': 'プロジェクトの詳細を入力（任意）'
            }),
            # 必要工数の入力欄（マイナス値を防ぐため min='0' を指定）
            'required_hours': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': '0',
                'placeholder': '例: 120'
            }),
        }

class AdminEmployeeCreateForm(UserCreationForm):
    """管理者が社員アカウントを作成するための専用フォーム"""
    class Meta(UserCreationForm.Meta):
        model = User
        # 管理者なので、最初から権限(role)も設定できるようにする
        fields = ('employee_number', 'last_name', 'first_name', 'role')