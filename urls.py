from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', views.login_view, name='login'),
#     path('dashboard/', views.dashboard_view, name='dashboard'),
#     path('api/upload/', views.upload_files_view, name='upload_files'),
#     path('api/settings/', views.save_settings_view, name='save_settings'),
#     path('admin-panel/', views.admin_panel_view, name='admin_panel'),
#     path('api/admin-action/', views.admin_action_view, name='admin_action'),

#     #############################################################

#     path('admin/', admin.site.urls),
#     path('super-admin/', views.super_admin_panel, name='super_admin_panel'),
#     path('api/super-admin-action/', views.super_admin_action, name='super_admin_action'),

#     ##############################################################

#     # در urlpatterns اضافه کنید:
#     path('admin-manager/', views.admin_manager_panel, name='admin_manager_panel'),
#     path('api/admin-action/', views.admin_action_api, name='admin_action_api'),
# ]

from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from core import views

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

# سرویس فایل‌های مدیا و استاتیک در حالت توسعه
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#/home/danial/Downloads/online-cafe-reservation-system-main/common /home/danial/Downloads/online-cafe-reservation-system-main/common/admin.py /home/danial/Downloads/online-cafe-reservation-system-main/common/models.py /home/danial/Downloads/online-cafe-reservation-system-main/config /home/danial/Downloads/online-cafe-reservation-system-main/media /home/danial/Downloads/online-cafe-reservation-system-main/menu /home/danial/Downloads/online-cafe-reservation-system-main/menu/migrations /home/danial/Downloads/online-cafe-reservation-system-main/menu/__init__.py /home/danial/Downloads/online-cafe-reservation-system-main/menu/admin.py /home/danial/Downloads/online-cafe-reservation-system-main/menu/apps.py /home/danial/Downloads/online-cafe-reservation-system-main/menu/choices.py /home/danial/Downloads/online-cafe-reservation-system-main/menu/models.py /home/danial/Downloads/online-cafe-reservation-system-main/menu/tests.py /home/danial/Downloads/online-cafe-reservation-system-main/menu/urls.py /home/danial/Downloads/online-cafe-reservation-system-main/menu/views.py /home/danial/Downloads/online-cafe-reservation-system-main/reservations /home/danial/Downloads/online-cafe-reservation-system-main/seating /home/danial/Downloads/online-cafe-reservation-system-main/seating/migrations /home/danial/Downloads/online-cafe-reservation-system-main/seating/__init__.py /home/danial/Downloads/online-cafe-reservation-system-main/seating/admin.py /home/danial/Downloads/online-cafe-reservation-system-main/seating/apps.py /home/danial/Downloads/online-cafe-reservation-system-main/seating/choices.py /home/danial/Downloads/online-cafe-reservation-system-main/seating/models.py /home/danial/Downloads/online-cafe-reservation-system-main/seating/tests.py /home/danial/Downloads/online-cafe-reservation-system-main/seating/views.py /home/danial/Downloads/online-cafe-reservation-system-main/seeds /home/danial/Downloads/online-cafe-reservation-system-main/static /home/danial/Downloads/online-cafe-reservation-system-main/templates /home/danial/Downloads/online-cafe-reservation-system-main/users /home/danial/Downloads/online-cafe-reservation-system-main/users/migrations /home/danial/Downloads/online-cafe-reservation-system-main/users/__init__.py /home/danial/Downloads/online-cafe-reservation-system-main/users/admin.py /home/danial/Downloads/online-cafe-reservation-system-main/users/apps.py /home/danial/Downloads/online-cafe-reservation-system-main/users/forms.py /home/danial/Downloads/online-cafe-reservation-system-main/users/models.py /home/danial/Downloads/online-cafe-reservation-system-main/users/tests.py /home/danial/Downloads/online-cafe-reservation-system-main/users/urls.py /home/danial/Downloads/online-cafe-reservation-system-main/users/views.py /home/danial/Downloads/online-cafe-reservation-system-main/venv /home/danial/Downloads/online-cafe-reservation-system-main/.$ERD.drawio.bkp /home/danial/Downloads/online-cafe-reservation-system-main/.gitignore /home/danial/Downloads/online-cafe-reservation-system-main/ERD.drawio /home/danial/Downloads/online-cafe-reservation-system-main/ERD.png /home/danial/Downloads/online-cafe-reservation-system-main/LICENSE /home/danial/Downloads/online-cafe-reservation-system-main/manage.py /home/danial/Downloads/online-cafe-reservation-system-main/README.md