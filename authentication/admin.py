from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email','first_name','last_name', 'phone_number']
    search_fields = ('first_name','last_name','username', 'email', 'phone_number')
