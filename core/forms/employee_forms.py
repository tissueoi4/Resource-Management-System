from django import forms
from core.models import TaskEffort, AvailableResource
from datetime import datetime


class AvailableResourceForm(forms.ModelForm):
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