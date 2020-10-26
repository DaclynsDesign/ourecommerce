from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)



class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False, seller=False):
        if not email:
            raise ValueError('User must have an email address')
        if not password:
            raise ValueError("User must enter a password")
        
        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active 
        user_obj.seller = seller 
        user_obj.save(using=self._db)
        return user_obj 

    def create_staffuser(self,email,password=None):
        user = self.create_user(
            email,password=password,is_staff=True
        )
        return user 

    def create_superuser(self,email,password=None):
        user = self.create_user(
            email,password=password,is_staff=True, is_admin=True
        )
        return user 

    def create_selleruser(self,email,password=None):
        user = self.create_user(
            email,password=password,is_active=True, seller=True
        )
        return user 



# Create your models here.
class User(AbstractBaseUser):
    # username = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True, default='newuser@gmail.com')
    #full_name = models.CharField(max_length=255,blank=True,null=True)
    active = models.BooleanField(default=True) #can login
    staff = models.BooleanField(default=False) #staff but not superuser
    admin = models.BooleanField(default=False) #superuser
    seller = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    '''
    Explicitly stating what our username shd be whether email or username
    '''
    USERNAME_FIELD = 'email' 

    #REQUIRED FIELDS WHEN USERS ARE BEING CREATED
    REQUIRED_FIELDS = [] #['fullname']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm,obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    @property
    def is_seller(self):
        return self.seller



#----------------------------------------------------------#
#GUEST EMAIL MODEL
class GuestEmailModel(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email