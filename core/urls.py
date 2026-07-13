# from django.urls import path

# from . import views
# from memo.views import views
# from memo.views.memo.views import MemoListView, MemoCreateView,  MemoUpdateView, MemoDeleteView
# app_name = 'memo'

# urlpatterns = [
#     path('memos', MemoListView.as_view(), name='list_memo'),
#     path('memos_edit/<int:pk>', MemoUpdateView.as_view(), name='edit_memo'),
#     path('memos_new', MemoCreateView.as_view(), name='create_memo'),
#     path('memos_delete/<int:pk>', MemoDeleteView.as_view(), name='delete_memo'),
# ]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('employee/', include('core.urls.employee_urls')),
    path('', include('core.urls')),
]