from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from core.forms.auth_forms import ProfileEditForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

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

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileEditForm
    template_name = 'core/auth/profile_edit.html' 
    
    success_url = reverse_lazy('profile_edit')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "プロフィール設定を更新しました。")
        return super().form_valid(form)