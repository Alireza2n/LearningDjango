from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from inventory import models as inventory_models


def add_to_cart(request, product_id):
    """
    Add a product to cart
    """
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
        request.session['cart'] = {
            # '1': 1
            # Product ID : Qty
        }

    # Method1
    if str(product_instance.pk) in request.session['cart'].keys():
        request.session['cart'][str(product_instance.pk)] += 1
    else:
        request.session['cart'][str(product_instance.pk)] = 1

    # Save the session!
    request.session.modified = True

    # Method 2
    # try:
    #     print(request.session['cart'][str(product_instance.pk)])
    #     request.session['cart'][str(product_instance.pk)] += 1
    # except KeyError:
    #     request.session['cart'][str(product_instance.pk)] = 1

    print(request.session['cart'])
    messages.success(
        request,
        f'کالای '
        f'{product_instance.name}'
        f' به سبد افزوده شد.'
    )
    return redirect('inventory:list')


def view_cart(request):
    """
    Renders the cart items (the basket)
    """
    object_list = []
    for item in request.session.get('cart', []):
        object_list += [
            {
                'product': inventory_models.Product.objects.get(pk=int(item)),
                'qty': request.session['cart'][item]
            }
        ]

    return render(
        request, 'store/view_cart.html', context={'object_list': object_list}
    )


def delete_row(request, product_id):
    """
    Deletes a product row from cart
    """
    request.session['cart'].pop(str(product_id), None)
    request.session.modified = True
    messages.success(request, 'حذف شد.')
    return redirect('store:view-cart')


@require_POST
@csrf_exempt
def deduct_from_cart(request):
    """
    Deducts one from product's qty in the cart
    """
    product_id = request.POST.get('product_id', None)

    # What if there were not product_id provided?
    if not product_id:
        return JsonResponse({'success': False, 'error': 'Invalid data.'}, status=400)

    # Try to deduct from qty
    try:
        request.session['cart'][product_id] -= 1
        request.session.modified = True
        return JsonResponse({'success': True, 'qty': request.session['cart'][product_id]}, status=200)
    except KeyError:
        # What if the product is not in the cart?
        return JsonResponse({'success': False, 'error': 'Invalid data. Not in the cart.'}, status=400)
