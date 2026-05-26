from django.db import models

class DateDecision(models.Model):
    CHOICES = (
        ('YES', 'Absolutely'),
        ('NO', 'Not a chance'),
    )
    voter_ip = models.GenericIPAddressField(null=True, blank=True)
    decision = models.CharField(max_length=3, choices=CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.decision} at {self.timestamp}"
