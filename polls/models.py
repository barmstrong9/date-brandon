from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class DateDecision(models.Model):
    CHOICES = (
        ('YES', 'Absolutely'),
        ('NO', 'Not a chance'),
    )
    voter_ip = models.GenericIPAddressField(null=True, blank=True)
    decision = models.CharField(max_length=3, choices=CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    feedback = models.CharField(max_length=200, null=True, blank=True)
    ladies_name = models.CharField(max_length=50, null=True, blank=True)
    instagram = models.CharField(max_length=30, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True, region="GB")

    def __str__(self):
        return f"{self.decision} at {self.timestamp}"
