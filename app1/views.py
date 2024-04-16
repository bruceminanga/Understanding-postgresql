# Import necessary modules from Django and local files
from django.shortcuts import render
from .forms import OrderForm, CouponApplyForm
from .models import Order, Coupon
from .utils import calculate_price
from django.utils import timezone

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

def home(request):
    # Render the HTML template index.html
    return render(request, "home.html")

# This function is called when PayPal sends a POST request after a payment is completed
@csrf_exempt
def paypal_ipn(request):
    # The data sent by PayPal can be accessed via request.POST
    # You can use this data to update your system, for example, to mark the order as paid
    print(request.POST)  # This is just for debugging, remove this in production
    return HttpResponse()

# This is a class-based view for handling coupon related requests
class CouponView(View):
    # This function is called when a GET request is made to this view
    def get(self, request, *args, **kwargs):
        # Get the coupon code from the URL parameters
        code = self.kwargs.get('code')
        try:
            # Try to get the coupon with the given code
            coupon = Coupon.objects.get(code=code)
            # Check if the coupon is valid
            if coupon.valid_from <= timezone.now() <= coupon.valid_to:
                # If valid, return a JSON response with the coupon's active status and discount
                return JsonResponse({'active': coupon.active, 'discount': coupon.discount})
            else:
                # If not valid, return a JSON response indicating that the coupon is not active
                return JsonResponse({'active': False})
        except Coupon.DoesNotExist:
            # If the coupon does not exist, return a JSON response indicating that the coupon is not active
            return JsonResponse({'active': False})

# This function handles order related requests
def order(request):
    price = None
    currency = None 
    academic_level = None
    coupon_apply_form = CouponApplyForm()  # Define here
    if request.method == 'POST':
        # If the request method is POST, it means the user has submitted the form
        form = OrderForm(request.POST)
        if form.is_valid():
            # If the form is valid, get the data from the form
            academic_level = form.cleaned_data['academic_level']
            service_type = form.cleaned_data['service_type']
            currency = form.cleaned_data['currency']
            # Calculate the price based on the academic level, service type, and currency
            price = calculate_price(academic_level, service_type, currency)
            # Save the form but don't commit to the database yet
            order = form.save(commit=False)
            # Assign the calculated price to the order's price field
            order.price = price
            # Now save the order to the database
            order.save()

        # Handle the coupon form
        form2 = CouponApplyForm(request.POST)
        if form2.is_valid():
            # If the form is valid, get the coupon code from the form
            code = form2.cleaned_data['coupon_code']
            now = timezone.now()
            try:
                # Try to get the coupon with the given code that is valid and active
                coupon = Coupon.objects.get(code__iexact=code,
                                            valid_from__lte=now,
                                            valid_to__gte=now,
                                            active=True)
                # If the coupon exists, store the coupon id in the session
                request.session['coupon_id'] = coupon.id
            except Coupon.DoesNotExist:
                # If the coupon does not exist, set the coupon id in the session to None
                request.session['coupon_id'] = None

    else:
        # If the request method is not POST, it means the user is requesting the form page
        form = OrderForm()
    # Render the order form page with the form, coupon form, price, currency, and academic level
    return render(request, 'order.html', {'form': form, 'coupon_apply_form': coupon_apply_form, 'price': price, 'currency':currency, 'academic_level':academic_level})
