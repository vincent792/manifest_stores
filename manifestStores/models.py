from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.

class Product(models.Model):
	product_name=models.CharField(max_length=255, unique=True)
	slug= models.SlugField(max_length=255, unique=True)
	description=models.TextField()
	price= models.IntegerField(default=0)
	old_price= models.IntegerField(default=0)
	images= models.ImageField(upload_to='photos/products')
	stock= models.IntegerField()
	# check if product is available
	is_available=models.BooleanField(default=True)
	category=models.ForeignKey(Category, on_delete=models.CASCADE)
	created_date=models.DateTimeField(auto_now_add=True)
	modified_date=models.DateTimeField(auto_now=True)
	sold=models.BooleanField()

	def get_url(self):
		return reverse('product_detail', args=[self.category.slug, self.slug ])


	def __str__(self):
		return self.product_name