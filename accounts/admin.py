from django.contrib import admin
from .models import Account,UserProfile
from django.contrib.auth.admin import UserAdmin

class AccountAdmin(UserAdmin):
    list_display=("first_name","username","is_active","email","date_joined","last_login")
    list_display_links = ('email', 'first_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    filter_horizontal=()
    list_filter=()
    fieldsets=()

class UserProfileAdmin(admin.ModelAdmin):
    list_display=['user', 'city', 'state', 'country']
    
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Account,AccountAdmin)
