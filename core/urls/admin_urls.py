from django.urls import path
from core.views import admin_views # 管理者用のビューだけを読み込む

urlpatterns = [
    # ここでは 'admin-dashboard/' ではなく 'dashboard/' だけでOKになります（理由は後述）
    path('dashboard/', admin_views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('projects/', admin_views.ProjectListView.as_view(), name='project_list'),
    path('projects/create/', admin_views.ProjectCreateView.as_view(), name='project_create'),
    path('employees/', admin_views.AdminEmployeeListView.as_view(), name='admin_employee_list'),
    path('resources/', admin_views.AdminResourceManagementView.as_view(), name='admin_resource_management'),
    path('employees/create/', admin_views.AdminEmployeeCreateView.as_view(), name='admin_employee_create'),
    path('employees/<int:pk>/role/', admin_views.AdminEmployeeRoleUpdateView.as_view(), name='admin_employee_role_update'),
    path('projects/<int:pk>/edit/', admin_views.ProjectUpdateView.as_view(), name='project_edit'),
    path('resources/<int:user_id>/<str:year_month>/edit/', admin_views.admin_resource_edit_view, name='admin_resource_edit'),
    path('efforts/<int:user_id>/<str:year_month>/create/', admin_views.AdminTaskEffortCreateView.as_view(), name='admin_effort_create'),
    path('efforts/<int:pk>/edit/', admin_views.AdminTaskEffortUpdateView.as_view(), name='admin_effort_edit'),
    path('efforts/<int:pk>/delete/', admin_views.AdminTaskEffortDeleteView.as_view(), name='admin_effort_delete'),
]