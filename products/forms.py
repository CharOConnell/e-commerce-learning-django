from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
        # includes all the fields

    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        # this is a nice way to create a list of tuples
        # syntax is called list comprehension so the for loop adds to the list

        self.fields['category'].choices = friendly_names
        # form will use the friendly names on the form
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
            # style the same as the rest of the site
