
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save 
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify 
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200,
    unique=True)
    
    def get_categories():
        return Category.objects.all()
  
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('product_list_by_category',
        args=[self.slug])
def uploaded_location(instance, filename):
    return ("%s/%s") %(instance.name,filename)


class Product(models.Model):
    image = models.ImageField(upload_to=uploaded_location)
    price = models.IntegerField(blank="False")
    old_price = models.IntegerField(blank=True, default=0)
    name = models.CharField(max_length=100)
    description =  models.TextField(blank=True)
    slug = models.SlugField(max_length=200, db_index=True)
    feature1 = models.CharField(max_length=60,blank=False, default='Feature')
    feature2 = models.CharField(max_length=60,blank=False, default='Feature')
    feature3 = models.CharField(max_length=60,blank=False, default='Feature')
    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    creator = models.ForeignKey(User, blank=True, null=True, related_name="%(class)s_posts", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('product_detail',
        args=[self.id, self.slug])
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)



class Profile(models.Model):
    category=(("Buyer",'Buyer'),
                ("Seller",'Seller'),
                 ("Admin",'Admin'),
                 
                )
    userpro= models.ForeignKey(User,on_delete=models.CASCADE)
    pro_pic= models.ImageField(blank=True, default='profile.jpg', upload_to='media/pro/')
    Role=models.CharField(max_length=20,choices = category,default="Buyer")
    bio=models.TextField(blank=True)

    def __str__(self):
        return self.userpro.username
    def apply(self):
        ap=Apply.objects.filter(profile=self).last()
        return ap

def createprofile (sender,**kwargs):
    if kwargs['created']:
        Profile.objects.create(userpro=kwargs['instance'])
       
post_save.connect(createprofile,sender=User)

class Apply(models.Model):
    profile= models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    documents= models.FileField( upload_to='media/apply/', validators=[FileExtensionValidator(allowed_extensions=['pdf','doc'])])
    applied=models.BooleanField(default=False)
    def __str__(self):
        return self.profile.userpro.username
    
    @property
    def accepted(self):
        profile=Profile.objects.filter(id=self.profile.id).last()
        if profile.category=="Buyer":
            return "Not accepted as buyer"
        else:
            return "accepted as seller"