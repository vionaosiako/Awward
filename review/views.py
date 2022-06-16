from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from .forms import  CreateUserForm,ProfileForm,ProjectForm,RatingForm
from .models import Profile,Project,Rating
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

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

def search_results(request):

    if 'project' in request.GET and request.GET["project"]:
        search_term = request.GET.get("project")
        searched_projects = Project.search_by_title(search_term).all()
        message = f"{search_term}"

        return render(request, 'search.html',{"message":message,"projects": searched_projects})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})
    

def project(request, project):
    user = Profile.objects.get(user=request.user)
    project = Project.objects.get(title=project)
    ratings = Rating.objects.filter(user=request.user.id, project=project).first()
    rating_status = None
    if ratings is None:
        rating_status = False
    else:
        rating_status = True
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user.profile
            rate.project = project
            rate.save()
            project_ratings = Rating.objects.filter(project=project)

            design_ratings = [d.design for d in project_ratings]
            design_average = sum(design_ratings) / len(design_ratings)

            usability_ratings = [us.usability for us in project_ratings]
            usability_average = sum(usability_ratings) / len(usability_ratings)

            content_ratings = [content.content for content in project_ratings]
            content_average = sum(content_ratings) / len(content_ratings)

            score = (design_average + usability_average + content_average) / 3
            print(score)
            rate.design_average = round(design_average, 2)
            rate.usability_average = round(usability_average, 2)
            rate.content_average = round(content_average, 2)
            rate.score = round(score, 2)
            rate.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = RatingForm()
    context = {
        'ratings':ratings,
        'form': RatingForm,
        'project': project,
        'rating_form': form,
        'rating_status': rating_status

    }
    return render(request, 'projectInfo.html', context)

    # def rating(request, project_id):
    #     user = Profile.objects.get(user=request.user)
    #     projects = Project.objects.get(id=project_id)
    #     ratings = Rating.objects.filter(user=request.user.id, project=project_id).first()
    #     rating_status=None
    #     if ratings is None:
    #         rating_status=False
    #     else:
    #         rating_status=True
    #     if request.method=='POST':
    #         form=RatingForm(request.POST)
    #         if form.is_valid():
    #             rate=form.save(commit=False)
    #             rate.user=request.user
    #             rate.project=projects
    #             rate.save()
    #             project_rating=Rating.objects.filter(project=Project)
    #             design_rating=[d.design for d in project_rating]
    #             content_rating=[c.content for c in project_rating]
    #             userbility_rating=[u.userbility for u in project_rating]
    #             average=(design_rating+content_rating+userbility_rating)/3
    #             rate.save()
    #             return HttpResponseRedirect(request.path_info)
    #     else:
    #         form=RatingForm()
    #     return render(request, 'projectInfo.html',{'form':RatingForm, 'projects':projects, 'rating_status':rating_status})
# def rating(request,project_id):
#     user = Profile.objects.get(user=request.user)
#     if request.method == "POST":
#         form=RatingForm(request.POST, request.FILES)
#         if form.is_valid():
#             data = form.save(commit=False)
#             # data.project=Project.objects.get(id=project_id)
#             data.profile = user
#             data.user=request.user.profile
#             data.save()
#             return redirect('index')
#         else:
#             form=ProjectForm()
    # projects = Project.objects.get(id=project_id)
    # current_user = request.user
    # if request.method == 'POST':
    #     form = RatingForm(request.POST,request.FILES,instance=projects)
    #     if form.is_valid:
    #         form.save(commit=False)
    #         form.user=request.user.profile
    #         form.project=Project.objects.get(id=project_id)
    #         form.save()
    #         return redirect('index')
    #return render(request, 'projectInfo.html',{'form':RatingForm})