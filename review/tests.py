from django.test import TestCase
from .models import Profile, Project
from django.contrib.auth.models import User


# Create your tests here.

class ProfileTestClass(TestCase):
    def setUp(self):
        
        self.user = User(username='riziki') 
        self.user.save()
        self.profile=Profile(user=self.user,fullname='viona',bio='Its me',profile_pic='')
        
        
    def tearDown(self):
        Profile.objects.all().delete()
        User.objects.all().delete()
        
    def test_instance(self):
        self.assertTrue(isinstance(self.profile,Profile))
        

class ProjectTestClass(TestCase):
    def setUp(self):
        self.user = User(username='collo') 
        self.user.save()
        # self.image=Image(id=1,image='',name='book', caption='Its amazing', date_posted='', user=self.profile)
        self.project=Project(id=1,title='PitchItUp',description='Its me',project_url='',date_posted='',user=self.profile)
        self.profile=Profile(user=self.user,fullname='viona',bio='Its me',profile_pic='')
    def tearDown(self):
        User.objects.all().delete()
        Project.objects.all().delete()
    
    def test_instance(self):
        self.assertTrue(isinstance(self.project,Project))
    
    # def test_save_project(self):
    #     saved_project=Project.objects.all().delete()
    #     self.assertTrue((len(saved_project))>0)
        
    # def test_delete_project(self):
    #     self.project.delete_project()
    #     delete_project=Project.objects.all()
    #     self.assertTrue(len(delete_project)==0)