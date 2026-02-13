import os
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UploadedFile, UserSettings
#from .models import UploadedFile


# --- Helper ---
def get_or_create_settings(user):
    settings, created = UserSettings.objects.get_or_create(user=user)
    return settings

# --- Login ---
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            return JsonResponse({'success': True, 'uid': user.id, 'role': 'admin' if user.is_staff else 'user'})
        else:
            return JsonResponse({'success': False, 'msg': 'نام کاربری یا رمز عبور اشتباه است'})
    return render(request, 'login.html')

# --- Dashboard ---
@login_required
def dashboard_view(request):
    settings = get_or_create_settings(request.user)
    # دریافت فایل‌های آپلود شده توسط کاربر برای نمایش در سمت چپ
    my_files = UploadedFile.objects.filter(uploaded_by=request.user, is_deleted=False).order_by('-uploaded_at')
    return render(request, 'dashboard.html', {'settings': settings, 'my_files': my_files})

# --- Upload API ---
@csrf_exempt
@login_required
def upload_files_view(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        folder_name = request.POST.get('folder_name', 'Unknown')
        
        uploaded_count = 0
        rejected_count = 0
        
        for f in files:
            if f.name.lower().endswith('.exe'):
                rejected_count += 1
                continue
                
            UploadedFile.objects.create(file=f, uploaded_by=request.user, folder_name=folder_name)
            uploaded_count += 1
            
        msg = f'{uploaded_count} فایل آپلود شد.'
        if rejected_count > 0:
            msg += f' {rejected_count} فایل EXE مجاز نبود و رد شد.'
            
        return JsonResponse({'success': True, 'msg': msg})
    
    return JsonResponse({'success': False, 'msg': 'خطا در آپلود'})

# --- Settings API ---
@csrf_exempt
@login_required
def save_settings_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        settings = get_or_create_settings(request.user)
        settings.font_size = int(data.get('font_size', 14))
        settings.menu_size = int(data.get('menu_size', 200))
        settings.button_size = int(data.get('button_size', 40))
        settings.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# --- Admin Panel ---
@login_required
def admin_panel_view(request):
    if not request.user.is_staff:
        return redirect('dashboard')
    
    users = User.objects.all()
    history = UploadedFile.objects.select_related('uploaded_by').all().order_by('-uploaded_at')
    return render(request, 'admin_panel.html', {'users': users, 'history': history})

# --- Admin Actions (Create User, Block, etc) ---
@csrf_exempt
@login_required
def admin_action_view(request):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'msg': 'Unauthorized'})
    
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        
        if action == 'create_user':
            username = data.get('username')
            password = data.get('password')
            is_staff = data.get('is_staff', False)
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'msg': 'نام کاربری تکراری است'})
                
            User.objects.create_user(username=username, password=password, is_staff=is_staff)
            return JsonResponse({'success': True, 'msg': 'کاربر جدید ساخته شد'})
            
        elif action == 'change_password':
            user = get_object_or_404(User, id=data.get('user_id'))
            user.set_password(data.get('new_password'))
            user.save()
            return JsonResponse({'success': True, 'msg': 'رمز عبور تغییر کرد'})
            
        elif action == 'block_user':
            user = get_object_or_404(User, id=data.get('user_id'))
            user.is_active = False
            user.save()
            return JsonResponse({'success': True, 'msg': 'کاربر مسدود شد'})
            
        elif action == 'unblock_user':
            user = get_object_or_404(User, id=data.get('user_id'))
            user.is_active = True
            user.save()
            return JsonResponse({'success': True, 'msg': 'کاربر آزاد شد'})
            
        elif action == 'delete_file':
            f = get_object_or_404(UploadedFile, id=data.get('file_id'))
            f.delete()
            return JsonResponse({'success': True, 'msg': 'فایل حذف شد'})
            
    return JsonResponse({'success': False, 'msg': 'Invalid action'})


########################################################################################
#for ___superadmin___ panel 
########################################################################################

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Permission, Group
from .models import UserProfile, PasswordPolicy
import json

# ویوی اصلی برای نمایش صفحه HTML
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission
from .models import PasswordPolicy

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission
from .models import PasswordPolicy
from django.contrib import messages


@login_required
def super_admin_panel(request):
    # چک کردن وضعیت کاربر
    print(f"User: {request.user.username}")
    print(f"Is superuser: {request.user.is_superuser}")
    print(f"Is staff: {request.user.is_staff}")
    print(f"Is authenticated: {request.user.is_authenticated}")
    
    # اگر کاربر سوپر ادمین نیست
    if not request.user.is_superuser:
        messages.error(request, "شما دسترسی به این صفحه را ندارید!")
        return redirect('/dashboard/')  # به داشبورد برگردان
    
    # اگر کاربر سوپر ادمین است، اجازه ورود بده
    try:
        # دریافت یا ایجاد تنظیمات سیاست رمز عبور
        policy, created = PasswordPolicy.objects.get_or_create(pk=1)
        
        # دریافت تمام پرمیشن‌ها
        all_perms = Permission.objects.all()
        
        # دریافت تمام کاربران به همراه پروفایل آن‌ها
        users = User.objects.select_related('userprofile').all()

        context = {
            'policy': policy,
            'all_perms': all_perms,
            'users': users,
        }
        return render(request, 'super_admin_panel.html', context)
    
    except Exception as e:
        print(f"Error: {e}")
        messages.error(request, f"خطا در بارگذاری صفحه: {e}")
        return redirect('/dashboard/')

# API برای انجام عملیات‌های AJAX
@csrf_exempt # برای سادگی در اینجا exempt گذاشتم، اما در تولید بهتر از CSRF Token استفاده شود
@login_required
def super_admin_action(request):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'msg': 'دسترسی غیرمجاز'}, status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')

            if action == 'update_policy':
                # به‌روزرسانی سیاست رمز عبور
                policy = PasswordPolicy.objects.first()
                if policy:
                    policy.min_password_length = data.get('min_length')
                    policy.require_uppercase = data.get('require_uppercase')
                    policy.require_digit = data.get('require_digit')
                    policy.require_special_char = data.get('require_special_char')
                    policy.save()
                    return JsonResponse({'success': True, 'msg': 'سیاست رمز عبور با موفقیت ذخیره شد.'})

            elif action == 'create_role_with_perms':
                # ساخت نقش جدید و اختصاص دسترسی‌ها
                role_name = data.get('role_name')
                perm_ids = data.get('permissions')

                if not role_name:
                    return JsonResponse({'success': False, 'msg': 'نام نقش نمی‌تواند خالی باشد.'})

                group, created = Group.objects.get_or_create(name=role_name)
                
                # پاک کردن دسترسی‌های قبلی (اختیاری)
                group.permissions.clear()
                
                # اضافه کردن دسترسی‌های جدید
                if perm_ids:
                    permissions = Permission.objects.filter(id__in=perm_ids)
                    group.permissions.set(permissions)
                
                return JsonResponse({'success': True, 'msg': f'نقش {role_name} با موفقیت ساخته شد.'})

        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)})

    return JsonResponse({'success': False, 'msg': 'درخواست نامعتبر است.'})


############################################################################################


@login_required
def admin_manager_panel(request):
    # بررسی اینکه آیا کاربر ادمین است یا خیر
    if not request.user.is_staff:
        return render(request, 'login.html') # اگر ادمین نیست بفرست به صفحه لاگین

    users = User.objects.all()
    # دریافت فایل‌هایی که حذف نشده‌اند
    history = UploadedFile.objects.filter(is_deleted=False) 
    
    context = {
        'users': users,
        'history': history,
    }
    return render(request, 'admin_manager.html', context) # نام فایل HTML جدیدی که فرستادید


#############################################################################################



@csrf_exempt
@login_required
def admin_action_api(request):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'msg': 'دسترسی غیرمجاز'})

    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        # ۱. ساخت کاربر جدید
        if action == 'create_user':
            username = data.get('username')
            password = data.get('password')
            is_staff = data.get('is_staff', False)
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'msg': 'این نام کاربری قبلاً گرفته شده است'})
            
            user = User.objects.create_user(username=username, password=password)
            user.is_staff = is_staff
            user.save()
            return JsonResponse({'success': True, 'msg': 'کاربر با موفقیت ساخته شد'})

        # ۲. تغییر رمز عبور
        elif action == 'change_password':
            user_id = data.get('user_id')
            new_pass = data.get('new_password')
            try:
                u = User.objects.get(id=user_id)
                u.set_password(new_pass)
                u.save()
                return JsonResponse({'success': True, 'msg': 'رمز عبور تغییر کرد'})
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'msg': 'کاربر یافت نشد'})

        # ۳. مسدود کردن کاربر
        elif action == 'block_user':
            user_id = data.get('user_id')
            User.objects.filter(id=user_id).update(is_active=False)
            return JsonResponse({'success': True, 'msg': 'کاربر مسدود شد'})

        # ۴. فعال کردن کاربر
        elif action == 'unblock_user':
            user_id = data.get('user_id')
            User.objects.filter(id=user_id).update(is_active=True)
            return JsonResponse({'success': True, 'msg': 'کاربر فعال شد'})

        # ۵. حذف فایل
        elif action == 'delete_file':
            file_id = data.get('file_id')
            try:
                f = UploadedFile.objects.get(id=file_id)
                f.is_deleted = True # نرم‌افزار حذف می‌کنیم (بهتر است از فایل سیستم پاک نکنیم مگر با اطمینان)
                f.save()
                # اگر می‌خواهید از روی هارد هم پاک شود:
                # f.file.delete()
                return JsonResponse({'success': True, 'msg': 'فایل حذف شد'})
            except UploadedFile.DoesNotExist:
                return JsonResponse({'success': False, 'msg': 'فایل یافت نشد'})

    return JsonResponse({'success': False, 'msg': 'درخواست نامعتبر'})
#######################################################################################################


from django.contrib.auth.models import User, Permission, Group
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PasswordPolicy, UserProfile
import json

# ===== توابع جدید برای پنل سوپر ادمین =====

@login_required
def create_role(request):
    """ایجاد نقش جدید"""
    if not request.user.is_superuser:
        return JsonResponse({'error': 'دسترسی ندارید'}, status=403)
    
    if request.method == 'POST':
        role_name = request.POST.get('role_name')
        
        if not role_name:
            messages.error(request, 'نام نقش نمی‌تواند خالی باشد')
            return redirect('super_admin_panel')
        
        try:
            # بررسی تکراری نبودن نام نقش
            if Group.objects.filter(name=role_name).exists():
                messages.error(request, f'نقش با نام "{role_name}" قبلاً وجود دارد')
            else:
                group = Group.objects.create(name=role_name)
                messages.success(request, f'نقش "{role_name}" با موفقیت ایجاد شد')
        except Exception as e:
            messages.error(request, f'خطا در ایجاد نقش: {str(e)}')
        
        return redirect('super_admin_panel')
    
    return redirect('super_admin_panel')


@login_required
def assign_role_to_user(request):
    """اختصاص نقش به کاربر"""
    if not request.user.is_superuser:
        return JsonResponse({'error': 'دسترسی ندارید'}, status=403)
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        role_id = request.POST.get('role_id')
        action = request.POST.get('action', 'add')
        
        try:
            user = User.objects.get(id=user_id)
            role = Group.objects.get(id=role_id)
            
            if action == 'add':
                user.groups.add(role)
                message = f'نقش {role.name} به کاربر {user.username} اضافه شد'
            else:
                user.groups.remove(role)
                message = f'نقش {role.name} از کاربر {user.username} حذف شد'
            
            return JsonResponse({'success': True, 'message': message})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'کاربر یافت نشد'}, status=404)
        except Group.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'نقش یافت نشد'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'متد نامعتبر'}, status=405)


@login_required
def toggle_user_block(request):
    """تغییر وضعیت مسدودیت کاربر"""
    if not request.user.is_superuser:
        return JsonResponse({'error': 'دسترسی ندارید'}, status=403)
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        
        try:
            user = User.objects.get(id=user_id)
            
            # اگر کاربر خودش باشه، اجازه مسدود کردن نده
            if user.id == request.user.id:
                return JsonResponse({'success': False, 'error': 'نمی‌توانید خودتان را مسدود کنید'}, status=400)
            
            profile, created = UserProfile.objects.get_or_create(user=user)
            
            # تغییر وضعیت مسدودیت
            profile.is_blocked = not profile.is_blocked
            if profile.is_blocked:
                from django.utils import timezone
                profile.blocked_at = timezone.now()
                # غیرفعال کردن کاربر
                user.is_active = False
            else:
                profile.blocked_at = None
                # فعال کردن کاربر
                user.is_active = True
            
            profile.save()
            user.save()
            
            status = 'مسدود' if profile.is_blocked else 'فعال'
            return JsonResponse({
                'success': True, 
                'message': f'کاربر {user.username} {status} شد',
                'is_blocked': profile.is_blocked
            })
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'کاربر یافت نشد'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'متد نامعتبر'}, status=405)


@login_required
def delete_user(request, user_id):
    """حذف کاربر"""
    if not request.user.is_superuser:
        return JsonResponse({'error': 'دسترسی ندارید'}, status=403)
    
    if request.method == 'POST':
        try:
            user = User.objects.get(id=user_id)
            
            # اگر کاربر خودش باشه، اجازه حذف نده
            if user.id == request.user.id:
                return JsonResponse({'success': False, 'error': 'نمی‌توانید خودتان را حذف کنید'}, status=400)
            
            username = user.username
            user.delete()
            
            return JsonResponse({'success': True, 'message': f'کاربر {username} با موفقیت حذف شد'})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'کاربر یافت نشد'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'متد نامعتبر'}, status=405)


@login_required
def edit_user(request, user_id):
    """صفحه ویرایش کاربر"""
    if not request.user.is_superuser:
        return redirect('login')
    
    user = get_object_or_404(User, id=user_id)
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        # ویرایش اطلاعات کاربر
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.is_active = request.POST.get('is_active') == 'on'
        user.is_staff = request.POST.get('is_staff') == 'on'
        user.save()
        
        # ویرایش پروفایل
        profile.first_name = user.first_name
        profile.last_name = user.last_name
        profile.national_code = request.POST.get('national_code', '')
        profile.save()
        
        messages.success(request, f'اطلاعات کاربر {user.username} با موفقیت به‌روزرسانی شد')
        return redirect('super_admin_panel')
    
    context = {
        'edit_user': user,
        'profile': profile,
        'all_roles': Group.objects.all(),
    }
    return render(request, 'edit_user.html', context)

# ===== پایان توابع جدید =====





@login_required
def save_permissions(request):
    """ذخیره دسترسی‌ها برای یک نقش"""
    if not request.user.is_superuser:
        return JsonResponse({'error': 'دسترسی ندارید'}, status=403)
    
    if request.method == 'POST':
        role_id = request.POST.get('role_id')
        permissions = request.POST.getlist('permissions')
        
        if not role_id:
            messages.error(request, 'لطفاً یک نقش انتخاب کنید')
            return redirect('super_admin_panel')
        
        try:
            role = Group.objects.get(id=role_id)
            # پاک کردن دسترسی‌های قبلی و تنظیم دسترسی‌های جدید
            role.permissions.clear()
            if permissions:
                role.permissions.set(permissions)
            
            messages.success(request, f'دسترسی‌ها برای نقش {role.name} با موفقیت ذخیره شد')
        except Group.DoesNotExist:
            messages.error(request, 'نقش مورد نظر یافت نشد')
        except Exception as e:
            messages.error(request, f'خطا: {str(e)}')
        
        return redirect('super_admin_panel')
    
    return redirect('super_admin_panel')
