from django.urls import path
from django.contrib.auth import views as django_auth_views
from core.views import auth_views

urlpatterns = [
    # ログイン・ログアウト・新規登録
    path('login/', django_auth_views.LoginView.as_view(template_name='core/auth/login.html'), name='login'),
    path('logout/', django_auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', auth_views.SignUpView.as_view(), name='signup'),
]