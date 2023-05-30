from django.contrib import admin

# Register your models here.
from  category.models import Category

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields={'slug': ('category_name',)}
	list_display=('category_name', 'slug', 'cat_image')
	search_fields=('category_name','slug')

admin.site.register(Category, CategoryAdmin)
