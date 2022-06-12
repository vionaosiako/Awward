from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from .forms import  CreateUserForm,ProfileForm,ProjectForm
from .models import Profile,Project
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from django.http import JsonResponse
from .serializers import ProfileSerializer,ProjectSerializer
from rest_framework.decorators import api_view
from rest_framework .response import Response
from rest_framework import status

# Create your views here.
def registerPage(request):
    form =  CreateUserForm()
    contex = {'form':form}
    if request.method == 'POST':
        form= CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            # messages.success(request, 'Account was created for ' + user)
            return redirect('profileUpdates')
    return render(request, 'auth/register.html', contex)

def loginPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username OR password is incorrect')
    contex = {}
    return render(request, 'auth/login.html', contex)
def logoutUser(request):
	logout(request)
	return redirect('loginPage')

@login_required(login_url='loginPage')
def profileUpdates(request):
    current_user=request.user
    profile = Profile.objects.filter(id=current_user.id).first()
    if request.method == 'POST':
        profileform = ProfileForm(request.POST,request.FILES,instance=profile)
        if  profileform.is_valid:
            profileform.save(commit=False)
            profileform.user=request.user
            profileform.save()
            return redirect('index')
    else:
        form=ProfileForm(instance=profile)
    return render(request,'addProfile.html',{'form':form})

@login_required(login_url='loginPage')
def profilePage(request,user_id):
        profile=Profile.objects.get(id=user_id)
        projects = request.user.profile.projects.all()
        contex = {'profile':profile, 'projects':projects}
        return render(request, 'profile.html', contex)

@login_required(login_url='loginPage')
def index(request):
    projects=Project.objects.all()
    context={'projects':projects}
    return render(request, 'index.html',context)

@api_view (['GET','POST'])
def profile_list(request):
    #get all profile
    #serialize them return
    #return json
    if request.method == 'GET':
        profile = Profile.objects.all()
        serializer = ProfileSerializer(profile, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ProfileSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201.CREATED)
        
@api_view (['GET','POST'])
def project_list(request):
    if request.method == 'GET':
        project = Project.objects.all()
        serializer = ProjectSerializer(project, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ProjectSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201.CREATED)
        
@login_required(login_url='loginPage')
def newProject(request):
    user = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form=ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.profile = user
            data.user=request.user.profile
            data.save()
            return redirect('index')
        else:
            form=ProjectForm()

    return render(request, 'addProject.html',{'form':ProjectForm})
