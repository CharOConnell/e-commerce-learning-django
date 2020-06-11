from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    name = 'checkout'

    def ready(self):
        # every time a line item is saved/deleted
        # we call our own custom model
        import checkout.signals
