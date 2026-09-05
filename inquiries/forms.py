from django import forms
from django.forms import inlineformset_factory
from .models import ContactSubmission, VideoCallBooking, Order, OrderItem


class StyledFormMixin:
    """Adds the design system's `form-control` class to every field widget."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (existing + ' form-control').strip()


class ContactForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'phone', 'email', 'product_interest', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email (optional)'}),
            'message': forms.Textarea(attrs={'placeholder': 'How can we help?', 'rows': 5}),
        }


class AppointmentForm(StyledFormMixin, forms.ModelForm):
    TIME_CHOICES = [
        ('11:00 AM', '11:00 AM'),
        ('12:00 PM', '12:00 PM'),
        ('1:00 PM', '1:00 PM'),
        ('2:00 PM', '2:00 PM'),
        ('3:00 PM', '3:00 PM'),
        ('4:00 PM', '4:00 PM'),
        ('5:00 PM', '5:00 PM'),
    ]

    preferred_time = forms.ChoiceField(choices=TIME_CHOICES, label='Preferred time')

    class Meta:
        model = VideoCallBooking
        fields = ['full_name', 'phone', 'preferred_date', 'preferred_time']
        labels = {'full_name': 'Name'}
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number'}),
            'preferred_date': forms.DateInput(attrs={'type': 'date'}),
        }


class OrderForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Order
        fields = ['reseller_name', 'phone', 'city', 'payment_method']
        widgets = {
            'reseller_name': forms.TextInput(attrs={'placeholder': 'Your name / shop name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
        }


class OrderItemForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'unit_price']


OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    extra=3,
    can_delete=True,
)
