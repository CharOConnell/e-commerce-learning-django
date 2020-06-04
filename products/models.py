from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=254)
    # represents the programmatic name
    # eg bed_bath
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    # for the front end - eg Bed & Bath

    def __str__(self):
        # string method that takes in category model
        return self.name

    def get_friendly_name(self):
        # model method to make it easy to return the name
        return self.friendly_name

class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    # takes in the foreign key from category, null in database, blank in forms, and if deleted set to null rather than deleting
    # each product has a sku, name and description, decimal fields of price and rating, and image url
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
