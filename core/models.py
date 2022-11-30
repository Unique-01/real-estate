from django.db import models
from django.contrib.auth.models import User
from cities_light.models import City, Country, Region
from smart_selects.db_fields import ChainedForeignKey
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver  # Import the receiver


# Create your models here.

PROPERTY_TYPE_CHOICES = [
    ('rent', 'For Rent'),
    ('sale', 'For Sale')
]


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(
        upload_to='profile_image/', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    contact_info = models.CharField(max_length=15, blank=True, null=True)
    about = models.TextField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.user


class Category(models.Model):
    category = models.CharField(max_length=1000)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category


class Property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              blank=True, null=True, related_name='owner_property')
    title = models.CharField('Property name', max_length=500)
    slug = models.SlugField()
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, default=165)
    region = ChainedForeignKey(Region, chained_field='country',
                               chained_model_field='country', show_all=False, auto_choose=True, sort=True)
    city = ChainedForeignKey(City, chained_field='region',
                             chained_model_field='region', show_all=False, auto_choose=True, sort=True)
    price = models.PositiveIntegerField('Sale or Rent Price')
    address = models.CharField(max_length=200, null=True, blank=True)
    property_type = models.CharField(
        max_length=10, choices=PROPERTY_TYPE_CHOICES, default='')
    area_size = models.PositiveIntegerField(null=True, blank=True)
    bedroom = models.PositiveSmallIntegerField(
        'bedrooms', null=True, blank=True)
    bathroom = models.PositiveSmallIntegerField(
        'bathrooms', null=True, blank=True)
    garage = models.PositiveSmallIntegerField('garages', null=True, blank=True)
    room = models.PositiveSmallIntegerField('rooms', null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    year_of_construction = models.DateField(null=True, blank=True)
    last_renovation = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=False)

    #  to auto generate the slug from the topic

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Property, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Properties'

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='property_image')
    image = models.FileField(upload_to='property_images')
