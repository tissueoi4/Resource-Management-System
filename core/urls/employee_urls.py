from django.urls import path
from core.views import employee_views

urlpatterns = [
    path('dashboard/', employee_views.EmployeeDashboardView.as_view(), name='employee_dashboard'),
    path('task-effort/add/', employee_views.TaskEffortCreateView.as_view(), name='task_effort_add'),
    path('resource/add/', employee_views.AvailableResourceCreateView.as_view(), name='resource_add'),
    path('effort/add/', employee_views.TaskEffortCreateView.as_view(), name='task_effort_create'),
]