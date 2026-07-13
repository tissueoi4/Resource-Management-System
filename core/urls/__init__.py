from django.urls import path, include
from core.views import auth_views

# 必ずこの名前 'urlpatterns' でリストとして定義してください
urlpatterns = [
    path('', auth_views.dashboard_redirect, name='dashboard_redirect'),
    path('auth/', include('core.urls.auth_urls')),
    path('admin-panel/', include('core.urls.admin_urls')),
    path('employee/', include('core.urls.employee_urls')),
]