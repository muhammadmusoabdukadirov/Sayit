from django.shortcuts import render, redirect
from .models import CarpetType, Order, VisitorCount, Review
from django.views.decorators.csrf import csrf_exempt

def index(request):
    carpets = CarpetType.objects.all()
    reviews = Review.objects.all().order_by('-created_at')

    if not request.COOKIES.get('visited'):
        VisitorCount.objects.create()
        new_visitor = True
    else:
        new_visitor = False

    total_visitors = VisitorCount.objects.count()

    context = {
        'carpets': carpets,
        'reviews': reviews,
        'total_visitors': total_visitors,
        'new_visitor': new_visitor,
    }

    response = render(request, 'app/index.html', context)
    if new_visitor:
        response.set_cookie('visited', 'yes', max_age=365*24*60*60)

    return response


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

        Order.objects.create(
            name=name,
            phone=phone,
            address=address,
            carpet_type=carpet_type,
            other_carpet_name=other_carpet_name,
            date=date,
            comment=comment
        )
        return redirect('index')
    return redirect('index')


def clients(request):
    orders = Order.objects.all().order_by('-id')
    return render(request, 'app/clients.html', {'orders': orders})
