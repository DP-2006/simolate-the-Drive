
# from django.contrib import admin
# from .models import UploadedFile, UserSettings, DownloaderFile, UserProfile, PasswordPolicy

# # برای نمایش UserProfile در کنار کاربر
# class UserProfileInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False
#     verbose_name_plural = 'پروفایل'

# class UserAdmin(admin.ModelAdmin):
#     inlines = (UserProfileInline, )

# # لغو ثبت قبلی و ثبت مجدد User برای اضافه کردن Inline
# from django.contrib.auth.models import User
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)

# admin.site.register(UploadedFile)
# admin.site.register(UserSettings)
# admin.site.register(DownloaderFile)
# admin.site.register(PasswordPolicy)
    

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),  # فقط یک بار
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('api/upload/', views.upload_files_view, name='upload_files'),
    path('api/settings/', views.save_settings_view, name='save_settings'),
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
    # path('api/admin-action/', views.admin_action_view, name='admin_action'),  // این یکی را غیرفعال کنید یا حذف
    path('super-admin/', views.super_admin_panel, name='super_admin_panel'),
    path('api/super-admin-action/', views.super_admin_action, name='super_admin_action'),
    path('admin-manager/', views.admin_manager_panel, name='admin_manager_panel'),
    path('api/admin-action/', views.admin_action_api, name='admin_action_api'),  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)