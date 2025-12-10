from django.shortcuts import render, redirect, get_object_or_404
from .forms import CarpetTypeForm,CustomUserCreationForm
from .models import CarpetType, Order
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from django.db.models import Count
from .models import VisitLog
from django.contrib.auth.models import User
from .telegram_bot import send_telegram_message   # 👈 Import qildik



def index(request):
    carpets = CarpetType.objects.all()

    # 🔥 Bugungi sana
    today = timezone.now().date()
    start_of_today = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    end_of_today = timezone.make_aware(datetime.combine(today, datetime.max.time()))

    # 🔥 Bugungi kirishlarni hisoblash
    today_visits = VisitLog.objects.filter(timestamp__range=(start_of_today, end_of_today))

    # 🔥 Bugun kirgan foydalanuvchilar
    today_logged_in_users = today_visits.filter(user__isnull=False).values('user').distinct()
    today_logged_in_user_ids = [item['user'] for item in today_logged_in_users]
    today_users = User.objects.filter(id__in=today_logged_in_user_ids)

    # 🔥 To'liq statistikani hisoblash
    stats = {
        # Bugungi kirishlar statistikasi
        'today_visits': today_visits.count(),
        'guests_today': today_visits.filter(user__isnull=True).count(),
        'users_today': today_logged_in_users.count(),
        'admins_today': today_users.filter(is_superuser=True).count(),
        'staff_today': today_users.filter(is_staff=True, is_superuser=False).count(),
        'customers_today': today_users.filter(is_staff=False, is_superuser=False).count(),

        # Buyurtmalar statistikasi
        'new_orders': Order.objects.filter(created_at__date=today, status='new').count(),
        'processing_orders': Order.objects.filter(created_at__date=today, status='processing').count(),
        'completed_orders': Order.objects.filter(created_at__date=today, status='completed').count(),

        # Umumiy buyurtmalar (ixtiyoriy)
        'total_orders': Order.objects.all().count(),
        'total_new_orders': Order.objects.filter(status='new').count(),
        'total_processing_orders': Order.objects.filter(status='processing').count(),
        'total_completed_orders': Order.objects.filter(status='completed').count(),
    }

    context = {
        'carpets': carpets,
        'stats': stats,
        'today_date': today,  # ixtiyoriy: bugungi sanani ko'rsatish uchun
    }

    response = render(request, 'app/index.html', context)
    return response

# ---------------------------------CREATE_ORDER------------------------------------

def create_order(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        carpet_type_id = request.POST.get("carpet_type")
        other_carpet_name = request.POST.get("other_carpet_name")
        date = request.POST.get("date")
        comment = request.POST.get("comment")

        carpet_type = CarpetType.objects.get(id=carpet_type_id) if carpet_type_id else None

        order = Order.objects.create(
            name=name,
            phone=phone,
            address=address,
            carpet_type=carpet_type,
            other_carpet_name=other_carpet_name,
            date=date,
            comment=comment
        )

        # 📩 Botga ketadigan xabar
        message = f"""
📦 *Yangi buyurtma!*

👤 Ism: *{name}*
📞 Telefon: *{phone}*
📍 Manzil: *{address}*
🧼 Gilam turi: *{carpet_type.name if carpet_type else other_carpet_name}*
📅 Sana: *{date}*
📝 Izoh: {comment}
"""

        # 🔥 Qo‘shimcha faylga yozilgan funksiya chaqirilyapti
        send_telegram_message(message)

        messages.success(request, "Buyurtma muvaffaqiyatli yuborildi!")
        return redirect('index')

    return redirect('index')


def clients(request):
    orders = Order.objects.all().order_by('-id')

    # Statistika hisoblash
    total_orders = orders.count()
    new_orders = orders.filter(status='new').count()
    processing_orders = orders.filter(status='processing').count()
    completed_orders = orders.filter(status='completed').count()

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'new_orders': new_orders,
        'processing_orders': processing_orders,
        'completed_orders': completed_orders,
    }
    return render(request, 'app/clients.html', context)


# AJAX orqali status yangilash
@csrf_exempt
def update_order_status(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        status = request.POST.get('status')

        if status in ['new', 'processing', 'completed']:
            order.status = status
            order.save()
            return JsonResponse({'success': True, 'status': status})
    return JsonResponse({'success': False}, status=400)

@require_POST
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('clients')

# -------------------------SOZLAMALAR--------------------------------------------
def sozlamalar(request):
    add_form = CarpetTypeForm(request.POST or None, prefix="add")
    update_form = None
    selected_carpet = None

    # Qo'shish
    if add_form.is_valid() and 'add-name' in request.POST:
        new_carpet = add_form.save()
        messages.success(request, f"{new_carpet.name} muvaffaqiyatli qo'shildi!")
        return redirect('sozlamalar')

    # Yangilash
    if 'update-id' in request.POST and request.POST['update-id']:
        carpet_id = request.POST.get('update-id')
        selected_carpet = get_object_or_404(CarpetType, id=carpet_id)
        update_form = CarpetTypeForm(request.POST, instance=selected_carpet, prefix="update")

        if 'update-name' in request.POST and update_form.is_valid():
            updated_carpet = update_form.save()
            messages.success(request, f"{updated_carpet.name} muvaffaqiyatli yangilandi!")
            return redirect('sozlamalar')
    else:
        update_form = CarpetTypeForm(prefix="update")

    # O'chirish – alohida, update-ga bog‘lamay
    if 'delete-id' in request.POST and request.POST['delete-id']:
        carpet_id = request.POST.get('delete-id')
        selected_carpet = get_object_or_404(CarpetType, id=carpet_id)
        carpet_name = selected_carpet.name
        selected_carpet.delete()
        messages.success(request, f"{carpet_name} muvaffaqiyatli o'chirildi!")
        return redirect('sozlamalar')

    context = {
        'add_form': add_form,
        'update_form': update_form,
        'carpets': CarpetType.objects.all(),
    }
    return render(request, 'app/sozlamalar.html', context)


def boshqaruv_view(request):
    register_form = CustomUserCreationForm()
    login_form = AuthenticationForm()

    if request.method == "POST":
        action = request.POST.get("action")

        # --- Register ---
        if action == "register":
            register_form = CustomUserCreationForm(request.POST)
            if register_form.is_valid():
                new_user = register_form.save()  # Foydalanuvchi saqlanadi
                messages.success(request,
                                 f"Xush kelibsiz, {new_user.username}! Siz muvaffaqiyatli ro‘yxatdan o‘tdingiz. Iltimos, login qiling.")
                return redirect("boshqaruv")
            else:
                messages.error(request, "Ro‘yxatdan o‘tishda xatolik yuz berdi!")

        # --- Login ---
        elif action == "login":
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f"Xush kelibsiz, {user.username}!")
                return redirect("index")
            else:
                messages.error(request, "Login yoki parol noto‘g‘ri!")

        # --- Logout ---
        elif action == "logout":
            if request.user.is_authenticated:
                username = request.user.username
                logout(request)
                messages.success(request, f"{username}, siz chiqdingiz!")
            return redirect("index")

    context = {
        "register_form": register_form,
        "login_form": login_form,
    }
    return render(request, "app/boshqaruv.html", context)


@login_required(login_url='boshqaruv')  # Mehmon bo'lsa boshqaruv login sahifasiga yo'naltiriladi
def profile_view(request):
    user = request.user
    profile = user.profile  # Profilni olamiz (Profile modeli bilan bog'liq)

    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        if avatar:
            profile.avatar = avatar
        profile.phone = phone
        profile.save()

        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

    return render(request, 'app/profile.html', {'user': user})


def get_dashboard_stats():
    today = timezone.now().date()
    start_of_today = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    end_of_today = timezone.make_aware(datetime.combine(today, datetime.max.time()))

    # Bugungi kirishlar
    today_visits = VisitLog.objects.filter(timestamp__range=(start_of_today, end_of_today))

    # Bugun kirmagan foydalanuvchilarni aniqlash
    today_logged_in_users = today_visits.filter(user__isnull=False).values('user').distinct()
    today_logged_in_user_ids = [item['user'] for item in today_logged_in_users]

    # Bugun kirgan foydalanuvchilar turkumlari
    today_users = User.objects.filter(id__in=today_logged_in_user_ids)

    stats = {
        'today_visits': today_visits.count(),
        'guests_today': today_visits.filter(user__isnull=True).count(),
        'users_today': today_logged_in_users.count(),
        'new_orders': Order.objects.filter(status='new').count(),
        'processing_orders': Order.objects.filter(status='processing').count(),
        'completed_orders': Order.objects.filter(status='completed').count(),

        # Bugungi faol foydalanuvchilar ro'yxati (qo'shimcha)
        'today_active_users': today_users.values('username', 'email')[:10]
    }

    return stats