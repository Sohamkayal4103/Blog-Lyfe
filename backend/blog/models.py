from email.policy import default
from django.db import models
from datetime import datetime
from django.template.defaultfilters import slugify

class Categories(models.TextChoices):
  WORLD = 'world'
  ENVIORNMENT = 'enviornment'
  TECHNOLOGY = 'technology'
  DESIGN = 'design'
  CULTURE = 'culture'
  BUSINESS = 'business'
  POLITICS = 'politics'
  OPINION = 'opinion'
  SCIENCE = 'science'
  HEALTH = 'health'
  STYLE = 'style'
  TRAVEL = 'travel'

class BlogPost(models.Model):
  title = models.CharField(max_length=50)
  slug = models.SlugField()
  category = models.CharField(max_length=50, choices=Categories.choices, default=Categories.WORLD)
  thumbanil = models.ImageField(upload_to='photos/%Y/%m/%d')
  excerpt = models.CharField(max_length=150)
  models = models.CharField(max_length=3)
  day = models.CharField(max_length=2)
  content = models.TextField()
  featured = models.BooleanField(default=False)
  date_created = models.DateTimeField(default=datetime.now, blank=True)


  def save(self, *args, **kwargs):
    orignal_slug = slugify(self.title)
    queryset = BlogPost.objects.all().filter(slug__iexact=orignal_slug).count()

    count = 1
    slug = orignal_slug
    while(queryset):
      slug = orignal_slug + '-' + str(count)
      count += 1
      queryset = BlogPost.objects.all().filter(slug__iexact=orignal_slug).count()

    self.slug = slug

    if self.featured:
      try:
        temp = BlogPost.objects.get(featured=True)
        if self != temp:
          temp.featured = False
          temp.save()
      except BlogPost.DoesNotExist:
        pass
# Create your models here.
