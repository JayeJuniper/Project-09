from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms import SelectMultiple
from django.utils import timezone

from .models import Menu, Item, Ingredient

class MenuForm(forms.ModelForm):
    expiration_date = forms.DateTimeField(
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
        widget=forms.SelectDateWidget(
            years=range(2019,2029)
        )
    )
    class Meta:
        model = Menu
        fields = [
            'season',
            'items',
            'expiration_date'
        ]

        widgets = {
            'items': SelectMultiple(),
        }

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data['expiration_date']
        if expiration_date and expiration_date <= timezone.now():
            raise forms.ValidationError(
                "Expiration date must be after current date"
        )
        return expiration_date