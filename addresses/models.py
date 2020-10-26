from django.db import models
from billings.models import BillingModel

# Create your models here.
class Address(models.Model):
    billing_profile = models.ForeignKey(BillingModel)
    address_line_1 = models.CharField(max_length=150)
    address_line_2 = models.CharField(null=True,blank=True,max_length=150)
    gps_address = models.CharField(null=True,blank=True,max_length=50)
    city_or_town = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return str(self.billing_profile)

    def get_address(self):
        return f"{self.address_line_1},\n{self.address_line_2 or ''}\n{self.gps_address or ''}\n{self.city_or_town}"