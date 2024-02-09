from django.db import models
from category.models import Category
from accounts.models import Account
from django.urls import reverse
from django.db.models import Avg, Count

# Create your models here.
class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    price           = models.IntegerField()
    images          = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
    #calculate average rating
    def average_rating(self):
        ratings=ReviewRatings.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))
        avg=0
        if ratings['average'] is not None:
            avg = float(ratings['average'])
        return avg
    
    def review_count(self):
        reviews=ReviewRatings.objects.filter(product=self,status=True).aggregate(count=Count('id'))
        count=0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
    
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)
    
variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)
    
class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value     = models.CharField(max_length=100)
    is_active           = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
    
class ReviewRatings(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review=models.TextField(max_length=100, blank=True)
    rating=models.FloatField()
    ip= models.CharField(max_length=50, blank=True)
    status=models.BooleanField(default=True)
    created_at=models.DateField(auto_now_add=True)
    update_at=models.DateField(auto_now=True)

    def __str__(self):
        return self.subject
    class Meta:
        verbose_name='ReviewRatings'
        verbose_name_plural='ReviewRatings'
    

class ProductGallery(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    images=models.ImageField(upload_to='photos/products')

    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name='ProductGallery'
        verbose_name_plural='ProductGallery'