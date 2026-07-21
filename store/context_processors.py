from django.db.models import Sum

from .models import Cart


def cart_length(request):
    if request.user.is_authenticated:
        length = Cart.objects.filter(user=request.user).aggregate(
            total=Sum('quantity'),
        )['total'] or 0
    else:
        length = 0
    return {'cart_length': length}
