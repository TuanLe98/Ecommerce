from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from.models import Project,Tag
from project.project_form.form import ProjectForm,ReviewForm
from project.utils.utils import search_project,paginator_project

def home(request):
    search_query, project = search_project(request)
    project,customer_range = paginator_project(request,project,3)

    context ={
        'search_query':search_query,
        'projects':project,
        'customer_range':customer_range
    }
    return render(request,'project/home_page.html',context)

def single_project(request,pk):
    project = Project.objects.get(id=pk)
    reviewForm = ReviewForm()

    if request.method == 'POST':
        reviewForm = ReviewForm(request.POST)
        review = reviewForm.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()

        project.getVoteCount

        return redirect('single-project',pk=project.id)
    context ={
        'project':project,
        'reviewForm':reviewForm,
    }
    return render(request,'project/single_project.html',context)

@login_required(login_url='login_user')
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(','," ").split()
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag,created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('home')
    context = {
        'form':form
    }
    return render(request,'project/project_form.html',context)

@login_required(login_url='login_user')
def update_project(request,pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(','," ").split()
        form = ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            form.save()
            for tag in newtags:
                tag,created = Tag.objects.get_or_create(name = tag)
                project.tags.add(tag)
            return redirect('home')
    context = {
        'form':form
    }
    return render(request,'project/project_form.html',context)

@login_required(login_url='login_user')
def delete_project(request,pk):
    project = Project.objects.get(id = pk)
    if request.method =='POST':
        project.delete()
        return redirect('account')
    context = {
        'project':project
    }
    return render(request, 'project/delete_project.html', context)