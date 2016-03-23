from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import admin


class ImportData(models.Model):
    name = models.CharField(max_length=128, unique=True, default = "Unnamed")
    file = models.FileField(upload_to='files/%Y/%m/%d')
     
    # from Eviatar Bach
    def save(self, *args, **kwargs):
        super(ImportData, self).save(*args, **kwargs)
        filename = self.file.url
         
    def __unicode__(self):      
        return self.name

class Er_Room(models.Model):
	address = models.CharField(max_length=256, default="123 street road")
	name = models.CharField(max_length=128, default="name")
	city = models.CharField(max_length=128, default="city")
	latitude = models.DecimalField(max_digits=9, decimal_places=6, default="00.000000")
	longitude = models.DecimalField(max_digits=9, decimal_places=6, default="00.000000")
	
	def save(self, *args, **kwargs):
		super(Er_Room, self).save(*args, **kwargs)
        
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    website = models.URLField(blank=True)
    show_email = models.NullBooleanField(default=False)
    posts = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


# Modified code for a forum (http://lightbird.net/dbe/forum1.html) for review system
class Review(models.Model):
    title = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.creator) + " - " + self.title

    def num_posts(self):
        return self.post_set.count()

    def num_replies(self):
        return self.post_set.count() - 1

    def last_post(self):
        if self.post_set.count():
            return self.post_set.order_by("created")[0]


class Post(models.Model):
    title = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    review = models.ForeignKey(Review)
    body = models.TextField(max_length=10000)
    busyness = models.CharField(max_length=10, default="N/A")
    cleanliness = models.CharField(max_length=10, default="N/A")
    bedside = models.CharField(max_length=10, default="N/A")
    location = models.CharField(max_length=1000, default="N/A")
    showemail = models.NullBooleanField(default=False)

    def __unicode__(self):
        return u"%s - %s - %s" % (self.creator, self.review, self.title)

    def short(self):
        return u"%s - %s\n%s" % (self.creator, self.title, self.created.strftime("%b %d, %I:%M %p"))
    short.allow_tags = True
    

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user"]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ["title", "creator", "created"]
    list_filter = ["creator"]


class PostAdmin(admin.ModelAdmin):
    search_fields = ["title", "creator"]
    list_display = ["title", "review", "creator", "created"]

