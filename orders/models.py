from django.db import models
from django.conf import settings
from products.models import Product
# Create your models here.
class Order(models.Model):
   
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    zip_code = models.CharField(max_length=20)
    instructions=models.TextField()
    paid = models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(blank=True, default=0)
    products=models.ManyToManyField(Product)
    quantity = models.IntegerField(default=1)
    class Meta:
        ordering = ('-created',)
        verbose_name = 'Orders'
        verbose_name_plural = 'Orders'
        
    def __str__(self):
        return 'Order {}'.format(self.id)
class Payment(models.Model):
    order = models.ForeignKey(Order,
                            related_name='items',
                            on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '{}'.format(self.id)
    def get_cost(self):
        return self.price * self.quantity