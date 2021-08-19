from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.
class AccountAdmin(UserAdmin):
	list_display =  ('username', 'email', 'auth_provider', 'email_verified', 'is_superuser', 'created_at', 'updated_at')
	search_fields = ('email', 'username')
	readonly_fields = ('id', 'created_at', 'updated_at')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

admin.site.register(User, AccountAdmin)