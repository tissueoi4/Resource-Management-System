# core/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, employee_number, password=None, **extra_fields):
        if not employee_number:
            raise ValueError('社員番号は必須です')
        user = self.model(employee_number=employee_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, employee_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN') 

        if extra_fields.get('is_staff') is not True:
            raise ValueError('スーパーユーザーは is_staff=True である必要があります。')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('スーパーユーザーは is_superuser=True である必要があります。')

        return self.create_user(employee_number, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrator'), 
        ('EMPLOYEE', 'Employee'),
    )
    username = None
    
    employee_number_validator = RegexValidator(
        regex=r'^\d{5}$', 
        message="社員番号は5桁の半角数字で入力してください。"
    )
    
    employee_number = models.CharField(
        max_length=5, 
        unique=True, 
        validators=[employee_number_validator], 
        verbose_name="社員番号"
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='EMPLOYEE')
    last_name = models.CharField(verbose_name="姓", max_length=30, blank=True, default="")
    first_name = models.CharField(verbose_name="名", max_length=30, blank=True, default="")
    
    USERNAME_FIELD = 'employee_number'
    REQUIRED_FIELDS = [] 

    objects = CustomUserManager()

    def __str__(self):
        if self.last_name or self.first_name:
            return f"{self.employee_number} ({self.last_name} {self.first_name})"
        return self.employee_number
    
    def get_full_name(self):
        full_name = f"{self.last_name} {self.first_name}".strip()
        if full_name:
            return full_name
        return self.employee_number

class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name="プロジェクト名")
    description = models.TextField(blank=True, verbose_name="詳細")
    required_hours = models.PositiveIntegerField(verbose_name="必要工数（時間）")
    
    def __str__(self):
        return self.name
    
class AvailableResource(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='available_resources')
    target_month = models.DateField(verbose_name="対象月") 
    available_hours = models.PositiveIntegerField(verbose_name="稼働可能時間")

    class Meta:
        unique_together = ('user', 'target_month')

class TaskEffort(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_efforts')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    target_month = models.DateField(verbose_name="対象月") 
    allocated_hours = models.PositiveIntegerField(verbose_name="今月の予定工数(時間)")

    class Meta:
        unique_together = ('user', 'project', 'target_month')