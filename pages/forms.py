from django import forms
from inquiries.forms import StyledFormMixin
from .models import Testimonial


class TestimonialForm(StyledFormMixin, forms.ModelForm):
    RATING_CHOICES = [
        (5, '5 - Excellent'),
        (4, '4 - Good'),
        (3, '3 - Average'),
        (2, '2 - Below Average'),
        (1, '1 - Poor'),
    ]

    rating = forms.ChoiceField(choices=RATING_CHOICES, label='Rating')

    class Meta:
        model = Testimonial
        fields = ['name', 'rating', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your experience with us', 'rows': 5}),
        }
