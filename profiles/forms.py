from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        # what we want to render
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes , remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        # set up the form as default
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        # cursor will start in the full name field
        for field in self.fields:
            if field != 'default_country':
                # we removed the placeholder for country but don't need a placeholder
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                    # add a star if it's required
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
                # set all the placeholders to the values in dict above
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            # add a future css class
            self.fields[field].label = False
            # remove labels as we have placeholders
