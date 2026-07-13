from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required

# ※ フォルダ構造に合わせてインポート（ファイル直置きを想定）
from core.forms import CustomSignUpForm 

class SignUpView(CreateView):
    """新規ユーザー登録ビュー"""
    form_class = CustomSignUpForm
    template_name = 'core/auth/signup.html' 
    success_url = reverse_lazy('login')

@login_required
def dashboard_redirect(request):
    """ログイン直後に権限を見て画面を振り分けるビュー"""
    if request.user.role == 'ADMIN' or request.user.is_superuser:
        return redirect('admin_dashboard')
    else:
        return redirect('employee_dashboard')