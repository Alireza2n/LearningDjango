from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from inventory import models as inventory_models


def add_to_cart(request, product_id):
    product_instance = get_object_or_404(inventory_models.Product, pk=product_id)

    # 1- Check if product is in stock
    if not product_instance.can_be_sold():
        messages.error(request, 'این محصول امکان فروش ندارد.')
        return redirect('inventory:list')

    # 2- Check if product can be sold
    if not product_instance.is_in_stock(1):
        messages.error(request, 'این محصول به تعداد مورد نظر موجود نیست.')
        return redirect('inventory:list')

    if 'cart' not in request.session.keys():
        request.session['cart'] = []

    request.session['cart'] += [{
        'product_id': product_instance.pk,
        'qty': 1
    }]

    print(request.session['cart'])
    messages.success(
        request,
        f'کالای '
        f'{product_instance.name}'
        f' به سبد افزوده شد.'
    )
    return redirect('inventory:list')


def view_cart(request):
    object_list = []
    for item in request.session['cart']:
        object_list += [
            {
                'product': inventory_models.Product.objects.get(pk=item['product_id']),
                'qty': item['qty']
            }
        ]

    return render(
        request, 'store/view_cart.html', context={'object_list': object_list}
    )
