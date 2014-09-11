import re
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    info=models.TextField(default='')
    overview=models.TextField(default='')
    def __unicode__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title
# Create your models here.
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    info=models.TextField()
    website = models.URLField(blank=True)
    balance=models.IntegerField(default=0)


    #picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
class Address(models.Model):
    user = models.OneToOneField(User)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip = models.CharField(max_length=15, blank=True)

    def __unicode__(self):
    	return '{0}, {1}'.format(self.address,self.city)

class Contact(models.Model):

    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)

    birthdate = models.DateField(blank=True,null=True)
    phone = models.CharField(max_length=25, blank=True)
    email = models.EmailField(blank=True)
    address = models.ForeignKey(Address, null=True)   
    def __unicode__(self):
    	return '{0}  {1} lived in {2}'.format(self.first_name,self.last_name,self.address)

class Tag(models.Model):
   'Tag model'
   title=models.CharField('tag title',max_length=2**6, unique=True)
   def __unicode__(self):
      return '#{0}'.format(self.title)
   def get_absolute_url(self):
      'returns absolute path for tag'
      return reverse('view_tag',kwargs={'tag_id':self.id})  

class Article(models.Model):
  'Article model'
  category = models.ForeignKey(Category)
  author=models.ForeignKey(User)
  pub_date=models.DateTimeField('published date',auto_now_add=True)
  title=models.CharField('Title',max_length=2**6)
  content=models.TextField()
  #data=models.CharField('este neviem',max_length=2**6)
  pattern=re.compile(r'#(?P<title>\w+)')
  tags=models.ManyToManyField('Tag',blank=True)
  voices=models.ManyToManyField('UserProfile',blank=True)
  
  def __unicode__(self):
     return '"{2}" at {1} by {0}'.format(self.author,self.pub_date,self.title)
  def get_absolute_url(self):
     'returns absolute path for article'   
     return reverse('view_article',kwargs={'article_id':self.id})
  # def save(self,**kwargs):
  #    'save the article'
  #    super(Article,self).save(self)
  #    tags=Article.pattern.findall(self.content)
  #    #select * from tag where title in ('tag1','tag2')
  #    tags_existing=list(Tag.objects.filter(title__in=tags))
  #    tags_existing_titles=[tag.title for tag in tags_existing]
  #    #append missing tags as newly created ones
  #    for tag in tags:
  #     # print('procesing '+tag)
  #      if tag not in  tags_existing_titles:
  #        tag_new=Tag.objects.create(title=tag)
  #        tags_existing.append(tag_new)
  #        #add tags directly as a list
  #        self.tags=tags_existing