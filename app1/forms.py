from django import forms
from app1.models import Order

class CouponApplyForm(forms.Form):
    coupon_code = forms.CharField()

class OrderForm(forms.ModelForm):
    ACADEMIC_LEVEL_CHOICES = [
        ('undergraduate', 'Undergraduate'),
        ('high_school', 'High School'),
        ('masters', 'Masters'),
        ('phd', 'PhD'),
    ]

    SERVICE_TYPE_CHOICES = [
        ('writing', 'Writing'),
        ('editing', 'Editing'),
        ('proofreading', 'Proofreading'),
    ]

    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('GBP', 'GBP'),
    ]

    INCREMENTAL_CHOICES = [(i, str(i)) for i in range(1, 11)]
    
    WRITER_CATEGORY_CHOICES = [
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('platinum', 'Platinum'),
    ]



    academic_level = forms.ChoiceField(choices=ACADEMIC_LEVEL_CHOICES)
    service_type = forms.ChoiceField(choices=SERVICE_TYPE_CHOICES)
    currency = forms.ChoiceField(choices=CURRENCY_CHOICES)
    powerpoint_slides = forms.IntegerField(min_value=1, max_value=10)
    writer_category = forms.ChoiceField(choices=WRITER_CATEGORY_CHOICES, widget=forms.RadioSelect)
    number_of_pages_increment = forms.IntegerField(min_value=1, max_value=10)


    class Meta:
            model = Order  # replace with your model
            fields = ['academic_level', 'service_type', 'currency']  # replace with your fields


        

        