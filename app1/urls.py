from django.urls import path
from . import views
from .views import CouponView

app_name = 'app1'

urlpatterns = [
    path('', views.order, name='order'),
    path('api/coupons/<str:code>', CouponView.as_view()),
    # path('payment/', views.payment, name='payment'),
    path('home/', views.home, name='home'),
]