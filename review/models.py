from django.db import models
from cloudinary.models import CloudinaryField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
import datetime as dt

# Create your models here.
class Profile(models.Model):
    profile_pic=CloudinaryField('image')
    fullname=models.CharField(max_length=100)
    bio=models.TextField()
    phone_number=models.CharField(max_length=100,null=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.user.username
    
    @classmethod
    def search_profile(cls, fullname):
        return cls.objects.filter(user__username__icontains=fullname).all()
    
    @receiver(post_save,sender=User)
    def createUserProfile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            
    @receiver(post_save,sender=User)
    def saveUserProfile(sender, instance, **kwargs):
        instance.profile.save()
    def saveProfile(self):
        self.user()
        
class Project(models.Model):
    title = models.CharField(max_length=100)
    image = CloudinaryField('image')
    description=models.TextField()
    project_url = models.CharField(max_length=1000)
    date_posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')
    
    @classmethod
    def search_by_title(cls,search_term):
        title = cls.objects.filter(title__icontains=search_term).all()
        return title
    
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-date_posted']
        
class Rating(models.Model):
    rating = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),(9,'9'),(10,'10'),)
    design = models.IntegerField(choices=rating, default=0, blank=True, null=True)
    usability = models.IntegerField(choices=rating, default=0, blank=True, null=True)
    content = models.IntegerField(choices=rating,default=0, blank=True, null=True)
    
    score = models.FloatField(default=0, blank=True)
    design_average = models.FloatField(default=0, blank=True)
    usability_average = models.FloatField(default=0, blank=True)
    content_average = models.FloatField(default=0, blank=True)
    
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='reviewer')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ratings')
    
    def __str__(self):
        return self.project.title
    @classmethod 
    def getRatings(cls, id):
        ratings=Rating.objects.filter(project_id=id).all()
        return ratings
