# takes request as an argument and returns dictionary
from category.models import Category
def menu_links(request):
	links= Category.objects.all()
	return dict(links=links)

# tell setting ur using contxt processors
# in templates