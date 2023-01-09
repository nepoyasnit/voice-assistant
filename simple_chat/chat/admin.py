from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Dialog, Message
User = get_user_model()


class MessageAdmin(admin.ModelAdmin):
    list_display = ('text', 'date', 'is_mine')
    list_display_links = ('text', 'date', 'is_mine')
    search_fields = ('text',)


admin.site.register(Dialog)
admin.site.register(Message, MessageAdmin)


@admin.register(User)  # register the model on the admin panel
class UserAdmin(UserAdmin):
    pass
