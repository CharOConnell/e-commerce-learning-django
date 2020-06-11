from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        # what we want to render
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                    'street_address1', 'street_address2',
                    'town_or_city', 'postcode', 'country',
                    'county',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes , remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        # set up the form as default
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        # cursor will start in the full name field
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
                # add a star if it's required
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            # set all the placeholders to the values in dict above
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            # add a future css class
            self.fields[field].label = False
            # remove labels as we have placeholders
