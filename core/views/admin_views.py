from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum, F
from django.contrib.auth import get_user_model

from django.contrib import messages
from django.views.generic import UpdateView
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from core.forms.admin_forms import EmployeeRoleForm
from core.forms import AdminEmployeeCreateForm

from core.models import Project
from core.forms.admin_forms import EmployeeRoleForm, ProjectForm
from django.db.models.functions import Coalesce

from django.utils import timezone
from django.db.models import Prefetch
from core.models import AvailableResource, TaskEffort
import datetime

User = get_user_model()

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.role == 'ADMIN'

class AdminDashboardView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'core/admin/dashboard.html'

class AdminEmployeeListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = 'core/admin/employee_list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        queryset = User.objects.exclude(is_superuser=True).order_by('employee_number')
        
        query = self.request.GET.get('q')
        
        # もしキーワードが入力されていたら、社員番号で絞り込む
        if query:
            queryset = queryset.filter(employee_number__icontains=query)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 検索したあとも検索窓に入力した文字を残しておくための設定
        context['query'] = self.request.GET.get('q', '')
        return context

class AdminEmployeeRoleUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = User
    form_class = EmployeeRoleForm
    template_name = 'core/admin/employee_role_form.html'
    success_url = reverse_lazy('admin_employee_list')

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, f"社員番号{user.employee_number} の権限を更新しました。")
        return redirect(self.success_url)

class AdminEmployeeCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = User
    form_class = AdminEmployeeCreateForm
    template_name = 'core/admin/employee_create.html'
    
    success_url = reverse_lazy('admin_employee_list') 

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, f"社員番号 {user.employee_number} のアカウントを作成しました。")
        return super().form_valid(form)


class ProjectListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Project
    template_name = 'core/admin/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        queryset = Project.objects.annotate(
            total_allocated=Coalesce(Sum('taskeffort__allocated_hours'), 0)
        ).annotate(
            unallocated=F('required_hours') - F('total_allocated')
        ).order_by('-id')

        # 検索機能の追加：URLに ?q=xxx があれば名前で絞り込む
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 検索窓に入力した文字を画面に残すための設定
        context['query'] = self.request.GET.get('q', '')
        return context

class ProjectCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'core/admin/project_form.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        messages.success(self.request, "新しいプロジェクトを登録しました！")
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'core/admin/project_form.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        messages.success(self.request, "プロジェクト情報を更新しました。")
        return super().form_valid(form)
    
class AdminResourceManagementView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = 'core/admin/resource_management.html'
    context_object_name = 'employees'

    def get_queryset(self):
        month_str = self.request.GET.get('month', timezone.now().strftime('%Y-%m'))
        try:
            target_date = timezone.datetime.strptime(month_str, '%Y-%m').date()
        except ValueError:
            target_date = timezone.now().date().replace(day=1)

        available_prefetch = Prefetch(
            'available_resources',
            queryset=AvailableResource.objects.filter(target_month__year=target_date.year, target_month__month=target_date.month),
            to_attr='month_available'
        )
        effort_prefetch = Prefetch(
            'task_efforts',
            queryset=TaskEffort.objects.filter(target_month__year=target_date.year, target_month__month=target_date.month).select_related('project'),
            to_attr='month_efforts'
        )

        # 社員番号順（order_by）に固定
        queryset = User.objects.prefetch_related(available_prefetch, effort_prefetch).exclude(is_superuser=True).order_by('employee_number')
        
        # 社員番号での検索処理を追加
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(employee_number__icontains=query)
        
        for user in queryset:
            user.available_hours = user.month_available[0].available_hours if user.month_available else 0
            user.allocated_hours = sum(effort.allocated_hours for effort in user.month_efforts)
            user.remaining_hours = user.available_hours - user.allocated_hours
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_month'] = self.request.GET.get('month', timezone.now().strftime('%Y-%m'))
        context['query'] = self.request.GET.get('q', '')
        return context

# 管理者用の工数編集View
class AdminTaskEffortUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = TaskEffort
    fields = ('project', 'allocated_hours')
    template_name = 'core/admin/task_effort_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 編集対象の工数データから、ユーザーと月情報を渡す
        context['target_user'] = self.object.user
        context['year_month_str'] = self.object.target_month.strftime('%Y-%m')
        return context

    def get_success_url(self):
        month_str = self.object.target_month.strftime('%Y-%m')
        return reverse_lazy('admin_resource_management') + f'?month={month_str}'

    def form_valid(self, form):
        messages.success(self.request, f"社員番号{self.object.user.employee_number} の工数を変更しました。")
        return super().form_valid(form)

# 管理者用の工数削除View
class AdminTaskEffortDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = TaskEffort

    def get_success_url(self):
        month_str = self.object.target_month.strftime('%Y-%m')
        return reverse_lazy('admin_resource_management') + f'?month={month_str}'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, f"社員番号{self.object.user.employee_number} の工数割り当てを削除しました。")
        return super().post(request, *args, **kwargs)

class AdminTaskEffortCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = TaskEffort
    fields = ('project', 'allocated_hours')
    template_name = 'core/admin/task_effort_form.html' 

    def form_valid(self, form):
        user_id = self.kwargs.get('user_id')
        year_month = self.kwargs.get('year_month')
        
        user = get_object_or_404(User, pk=user_id)
        year, month = map(int, year_month.split('-'))
        target_date = datetime.date(year, month, 1)
        
        form.instance.user = user
        form.instance.target_month = target_date
        
        messages.success(self.request, f"社員番号{user.employee_number} に新しいプロジェクト工数を割り当てました。")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('admin_resource_management') + f"?month={self.kwargs.get('year_month')}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_user'] = get_object_or_404(User, pk=self.kwargs.get('user_id'))
        context['year_month_str'] = self.kwargs.get('year_month')
        return context

def admin_resource_edit_view(request, user_id, year_month):
    user = get_object_or_404(User, pk=user_id)
    year, month = map(int, year_month.split('-'))
    target_date = datetime.date(year, month, 1)

    resource, created = AvailableResource.objects.get_or_create(
        user=user,
        target_month=target_date,
        defaults={'available_hours': 100} 
    )

    if request.method == 'POST':
        new_hours = request.POST.get('available_hours')
        if new_hours is not None:
            resource.available_hours = int(new_hours)
            resource.save()
            messages.success(request, f"社員番号{user.employee_number} の{year_month}の稼働枠を更新しました。")
            return redirect(f"{reverse_lazy('admin_resource_management')}?month={year_month}")

    return render(request, 'core/admin/resource_edit.html', {
        'resource': resource,
        'target_user': user,
        'year_month': year_month
    })