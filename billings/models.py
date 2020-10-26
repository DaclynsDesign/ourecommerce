from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from accounts.models import GuestEmailModel

User = settings.AUTH_USER_MODEL

class BillingModelManager(models.Manager):
        def new_or_get(self,request):
                user=request.user
                guest_email_id = request.session.get('guest_email_id')

                created =False
                obj=None
                if user.is_authenticated():
                        '''Login user check out;remember payment stuff'''
                        obj, created = self.model.objects.get_or_create(user=user, 
                                      email=user.email)
                elif guest_email_id is not None:
                        '''Guest user check out; auto reloads payment stuff'''
                        guest_email_obj = GuestEmailModel.objects.get(id=guest_email_id)
                        obj, created = self.model.objects.get_or_create(
                        email=guest_email_obj.email)
                else:
                        pass
                return obj, created

# Create your models here.
class BillingModel(models.Model):
    user = models.OneToOneField(User, blank=True, null=True)
    email = models.CharField(max_length=50)
    active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    #Customer mobile money id 

    objects = BillingModelManager()


    def __str__(self):
        return self.email 




#Creating a billing profile when a user is also created
def user_create_billing(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingModel.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_create_billing, sender=User)