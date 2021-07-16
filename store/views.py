import logging

import weasyprint
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotAuthenticated

from inventory import models as inventory_models
from . import models, serializers, permissions

logger = logging.getLogger(__name__)


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

    # Cast product_id to string
    product_id = str(product_id)

    # Try to deduct from qty
    try:
        request.session['cart'][product_id] -= 1
        request.session.modified = True
        return JsonResponse({'success': True, 'qty': request.session['cart'][product_id]}, status=200)
    except KeyError:
        # What if the product is not in the cart?
        return JsonResponse({'success': False, 'error': 'Invalid data. Not in the cart.'}, status=400)


"""
DRF Views
"""


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for store.Order
    """
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.IsOwner]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_anonymous:
            raise NotAuthenticated('You need to be logged on.')
        return qs.filter_by_owner(self.request.user)

    @action(detail=True, description='Cancels an order')
    def cancel_order(self, request, *args, **kwargs):
        """
        Cancels an order
        """
        order_instance = self.get_object()
        order_instance.set_as_canceled()
        order_serializer = self.get_serializer(instance=order_instance)
        return JsonResponse(order_serializer.data, status=status.HTTP_202_ACCEPTED)


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for store.Order
    """
    queryset = models.OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer
    permission_classes = [permissions.IsOwnerOfParent]


@login_required
def finalize_order(request):
    """
    Finalize order
    """
    cart = request.session.get('cart', None)

    # If cart does not exist or is empty
    if not cart:
        messages.error(request, 'سبد شما خالی است.')
        return redirect('inventory:list')

    order_instance = models.Order.objects.create(owner=request.user)

    for product_id in cart:
        product = inventory_models.Product.objects.get(pk=product_id)
        qty = cart[product_id]

        if not product.is_in_stock(qty):
            messages.error(request, 'کالا به تعداد درخواست شده موجود نیست.')
            return redirect('store:view-cart')

        models.OrderItem.objects.create(
            order=order_instance,
            qty=qty,
            product=product,
            price=product.price
        )

        # Deduct from stock
        product.deduct_from_stock(qty)

    messages.info(request, 'سفارش با موفقیت ثبت شد.')
    request.session.pop('cart')
    logger.info(f"User #{request.user.pk} placed the order #{order_instance.pk}.")

    # or
    # del request.session['cart']
    request.session.modified = True
    return redirect('inventory:list')


class ListOrdersView(LoginRequiredMixin, ListView):
    model = models.Order
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(owner=self.request.user)
        return qs


class PrintOrder(LoginRequiredMixin, DetailView):
    model = models.Order

    def get(self, request, *args, **kwargs):
        # Call parents as normal
        g = super(PrintOrder, self).get(request, *args, **kwargs)

        # Get the rendered content and pass it to weasyprint
        rendered_content = g.rendered_content
        pdf = weasyprint.HTML(string=rendered_content).write_pdf()

        # Create a new http response with pdf mime type
        response = HttpResponse(pdf, content_type='application/pdf')
        return response
