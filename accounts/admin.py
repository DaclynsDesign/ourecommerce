from django.contrib import admin
from .models import GuestEmailModel
from django.contrib.auth import get_user_model
from .forms import UserAdminChangeForm, UserAdminCreationForm

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group


User = get_user_model()


# Register your models here.
class GuestEmailModelAdmin(admin.ModelAdmin):
    search_fields=['email']
    class Meta:
        model= GuestEmailModel

admin.site.register(GuestEmailModel, GuestEmailModelAdmin)


#------------------------------------------------#
class UserAdmin(BaseUserAdmin):
    form  = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('email','admin','staff')
    list_filter = ('admin','seller','active')
    fieldsets = (
        (None, {'fields':('email','password')}),
        ("Personal Info",{'fields':()}),
        ("Permissions",{'fields':('admin','staff','active','seller')}),
    )

    add_fieldsets = (
        (None,{
            'classes':("wide",),
            'fields':('email','password1','password2')
            }
        ),
    )
    search_fields =('email',)
    ordering = ("email",)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)