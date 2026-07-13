from django import forms
from core.models import TaskEffort, AvailableResource
from datetime import datetime


class AvailableResourceForm(forms.ModelForm):
    # input_formatsを指定するだけで、Djangoが自動で 2026-07 を 2026-07-01 にしてくれます！
    target_month = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'month', 'class': 'form-control'}),
        input_formats=['%Y-%m'], 
        label="対象月"
    )

    class Meta:
        model = AvailableResource
        fields = ('target_month', 'available_hours')
        widgets = {
            'available_hours': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }

class TaskEffortForm(forms.ModelForm):
    # 月の入力（2026-07）を自動的に日付（2026-07-01）に変換する魔法
    target_month = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'month', 'class': 'form-control'}),
        input_formats=['%Y-%m'], 
        label="対象月"
    )

    class Meta:
        model = TaskEffort
        fields = ('project', 'target_month', 'allocated_hours')
        widgets = {
            'project': forms.Select(attrs={'class': 'form-select'}),
            'allocated_hours': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }