from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from datetime import datetime
from django.shortcuts import redirect
from django.contrib import messages

from core.models import TaskEffort, AvailableResource
from core.forms import TaskEffortForm, AvailableResourceForm

class EmployeeDashboardView(LoginRequiredMixin, TemplateView):
    """一般社員用ダッシュボードビュー"""
    template_name = 'core/employee/dashboard.html' 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # ログインユーザーの合計稼働可能時間を取得
        context['total_available'] = AvailableResource.objects.filter(
            user=self.request.user
        ).aggregate(Sum('available_hours'))['available_hours__sum'] or 0
        
        # ログインユーザーの合計予定工数を取得
        context['total_effort'] = TaskEffort.objects.filter(
            user=self.request.user
        ).aggregate(Sum('allocated_hours'))['allocated_hours__sum'] or 0
        
        return context

class TaskEffortCreateView(LoginRequiredMixin, CreateView):
    """工数入力ビュー"""
    model = TaskEffort
    form_class = TaskEffortForm
    template_name = 'core/employee/task_effort_form.html'
    success_url = reverse_lazy('employee_dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)

class AvailableResourceCreateView(LoginRequiredMixin, CreateView):
    model = AvailableResource
    form_class = AvailableResourceForm
    template_name = 'core/employee/resource_form.html'
    success_url = reverse_lazy('employee_dashboard')

    def form_valid(self, form):
        target_month = form.cleaned_data['target_month']
        available_hours = form.cleaned_data['available_hours']

        AvailableResource.objects.update_or_create(
            user=self.request.user,
            target_month=target_month,
            defaults={'available_hours': available_hours}
        )
        
        messages.success(self.request, "稼働枠を保存しました！")
        return redirect(self.success_url)