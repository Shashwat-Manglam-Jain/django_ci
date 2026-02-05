from django.contrib import admin
from .models import User



admin.site.site_header = 'My administration'
admin.site.site_title = 'Ecommerce Admin Portal'
admin.site.index_title = 'Welcome to Ecommerce Admin Portal'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'roles', 'email', )
    list_filter = ('roles',)
