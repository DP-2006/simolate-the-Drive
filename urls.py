from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views
from django.conf import settings



# this url is not correct thanks for wating ti debuging! 
urlpatterns = [
    # صفحه اصلی (login)
    path('', views.login_view, name='login'),
    
    # ادمین جنگو - فقط یک بار
    path('admin/', admin.site.urls),
    
    # سایر صفحات
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
    path('super-admin/', views.super_admin_panel, name='super_admin_panel'),
    path('admin-manager/', views.admin_manager_panel, name='admin_manager_panel'),
    
    # APIها
    path('api/upload/', views.upload_files_view, name='upload_files'),
    path('api/settings/', views.save_settings_view, name='save_settings'),
    path('api/admin-action/', views.admin_action_view, name='admin_action'),
    path('api/super-admin-action/', views.super_admin_action, name='super_admin_action'),
]

# سرویس فایل‌های مدیا و استاتیک در حالت توسعه
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # برای رفع مشکل 404 در مسیرهای مستقیم
    from django.views.static import serve
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]





from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    # صفحه اصلی (login)
    path('', views.login_view, name='login'),
    
    # ادمین جنگو
    path('admin/', admin.site.urls),
    
    # صفحات اصلی
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
    path('super-admin/', views.super_admin_panel, name='super_admin_panel'),
    path('admin-manager/', views.admin_manager_panel, name='admin_manager_panel'),
    
    # APIها و عملیات‌ها
    path('api/upload/', views.upload_files_view, name='upload_files'),
    path('api/settings/', views.save_settings_view, name='save_settings'),
    path('api/admin-action/', views.admin_action_view, name='admin_action'),
    path('api/super-admin-action/', views.super_admin_action, name='super_admin_action'),
    
    # ===== مسیرهای جدید برای پنل سوپر ادمین =====
    # ایجاد نقش جدید
    path('api/create-role/', views.create_role, name='create_role'),
    
    # اختصاص نقش به کاربر
    path('api/assign-role/', views.assign_role_to_user, name='assign_role'),
    
    # تغییر وضعیت مسدودیت کاربر
    path('api/toggle-block/', views.toggle_user_block, name='toggle_block'),
    
    # حذف کاربر
    path('api/delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    
    # ویرایش کاربر
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    # به urls.py اضافه کن
    path('api/save-permissions/', views.save_permissions, name='save_permissions'),
    # ===========================================
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

