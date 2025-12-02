from django.shortcuts import render
from .models import CarpetType, Order, VisitorCount, Review

def index(request):
    orders = Order.objects.all()
    carpets = CarpetType.objects.all()
    reviews = Review.objects.all().order_by('-created_at')

    if not request.COOKIES.get('visited'):
        VisitorCount.objects.create()
        new_visitor = True
    else:
        new_visitor = False

    total_visitors = VisitorCount.objects.count()

    context = {
        'orders': orders,
        'carpets': carpets,
        'reviews': reviews,
        'total_visitors': total_visitors,
        'new_visitor': new_visitor,
    }

    response = render(request, 'app/index.html', context)
    if new_visitor:
        response.set_cookie('visited', 'yes', max_age=365*24*60*60)

    return response
