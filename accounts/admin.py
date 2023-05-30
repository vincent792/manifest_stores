from django.contrib import admin
from accounts.models import Account

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
	list_display=('email', 'username','phone', 'first_name', 'last_name','date_joined', 'last_login', 'is_active'  )
	list_display_links=('email','username', 'phone')
	readonly_fields=('last_login','date_joined', 'password')
	list_filter=()
	fieldsets=()

admin.site.register(Account, AccountAdmin)

