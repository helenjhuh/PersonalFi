from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import GameProfile, GameItem


class GameProfileInline(admin.StackedInline):
    model = GameProfile
    can_delete = False
    verbose_name_plural = "game profiles"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (GameProfileInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(GameItem)
