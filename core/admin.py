# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Project, AvailableResource, TaskEffort



class CustomUserAdmin(UserAdmin):
    model = User
    
    # 一覧画面での表示項目
    list_display = ('employee_number', 'last_name', 'first_name', 'role', 'is_staff')
    
    # 検索ボックスの対象
    search_fields = ('employee_number', 'last_name', 'first_name')
    
    # 並び順（社員番号順にする）
    ordering = ('employee_number',)

    # ユーザー詳細・編集画面のレイアウト
    fieldsets = (
        (None, {'fields': ('employee_number', 'password')}),
        ('プロフィール', {'fields': ('last_name', 'first_name', 'role')}),
        ('権限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('重要な日付', {'fields': ('last_login', 'date_joined')}),
    )

    # ユーザー新規追加画面のレイアウト
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('employee_number', 'last_name', 'first_name', 'role'),
        }),
    )

# カスタムした設定でUserモデルを登録
admin.site.register(User, CustomUserAdmin)


admin.site.register(Project)
admin.site.register(AvailableResource)
admin.site.register(TaskEffort)