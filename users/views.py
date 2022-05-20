from django.contrib.auth.models import User,Group
from django.contrib.auth import login,logout,authenticate, get_user_model
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse

from .models import Profile
from project.utils.utils import paginator_project
from users.utils.token import account_activation_token
from users.user_form.form import UserForm,ProfileForm,SkillForm,MessageForm
from users.utils.utils import search_profile,paginator_profile
from .utils.decorators import unauthenticated_user,allowed_users

@unauthenticated_user
def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            print('Username is not exist!')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            #return redirect(request.GET['next'] if 'next' in request.GET else 'home')
            return redirect(request.GET['next'] if 'next' in request.GET else 'home')
        else:
            print("Username or Password does not exist!")

    return render(request,'users/login_user.html')

def send_active_email(request,form,user):
    # create link activate to send to customer
    current_site = get_current_site(request)
    mail_subject = 'Activate your account'
    message = render_to_string('activation_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })

    # send activate email to customer
    to_email = form.cleaned_data.get('email')
    send_mail(
        mail_subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email]
    )

@unauthenticated_user
def registerUser(request):
    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.is_active = False
            user.save()
            send_active_email(request,form,user)
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            return HttpResponse('Please confirm your email address to complete the registration')
        return redirect('login_user')
    context ={
        'form':form,
    }
    return render(request,'users/register_user.html',context)


def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login_user')
@allowed_users(allowed_roles=['admin'])
def deleteUser(request,pk):
    profile = Profile.objects.get(id=pk)
    if request.method == 'POST':
        profile.delete()
        return redirect('profile')
    context = {
        'profile':profile
    }
    return render(request,'users/delete_user.html',context)

def profiles(request):
    search_query, profiles = search_profile(request)
    profiles,customer_range = paginator_profile(request,profiles,3)
    context ={
        'profiles':profiles,
        'search_query':search_query,
        'customer_range':customer_range,
    }
    return render(request, 'users/profile.html',context)

def single_profiles(request,pk):
    single_profile = Profile.objects.get(id=pk)
    #projects = Project.objects.all()
    projects = single_profile.project_set.all()
    projects,customer_range = paginator_project(request,projects,4)
    topskill = single_profile.skill_set.exclude(description__exact="")
    otherskill = single_profile.skill_set.filter(description="")
    context ={
        'single_profile':single_profile,
        'topskills':topskill,
        'otherskills':otherskill,
        'projects':projects,
        'customer_range':customer_range,
    }
    return render(request,'users/single_profile.html',context)


@login_required(login_url='login_user')
def update_profile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context ={
        'form':form
    }
    return render(request,'users/update_profile.html',context)

@login_required(login_url='login_user')
def account(request):
    profile = request.user.profile
    projects = profile.project_set.all()
    projects,customer_range = paginator_project(request,projects,4)
    topskills = profile.skill_set.exclude(description__exact="")
    otherskills = profile.skill_set.filter(description="")
    context = {
        'profile':profile,
        'topskills':topskills,
        'otherskills':otherskills,
        'projects':projects,
    }
    return render(request,'users/account.html',context)

@login_required(login_url='login_user')
def create_skill(request):
    skillForm = SkillForm()
    profile = request.user.profile

    if request.method == 'POST':
        skillForm = SkillForm(request.POST)
        if skillForm.is_valid():
            skill = skillForm.save(commit=False)
            skill.owner=profile
            skill.save()
            return redirect('account')
    context ={
        'skillForm':skillForm
    }
    return render(request,'users/skill.html',context)

@login_required(login_url='login_user')
def update_skill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {
        'skillForm':form
    }
    return render(request,'users/skill.html',context)

@login_required(login_url='login_user')
def delete_skill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        return redirect('account')
    context = {
        'skill':skill
    }
    return render(request,'users/delete_skill.html',context)

@login_required(login_url='login_user')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount=messageRequests.filter(is_read=False).count()
    context ={
        'messageRequests':messageRequests,
        'unreadCount':unreadCount,
    }
    return render(request,'users/inbox.html',context)

@login_required(login_url='login_user')
def message(request,pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context ={
        'message':message,
    }

    return render(request,'users/message.html',context)

@login_required(login_url='login_user')
def created_message(request,pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm(request.POST)

    try:
        sender = request.user.profile
    except:
        sender = None

    if form.is_valid():
        message = form.save(commit=False)
        message.sender = sender
        message.recipient = recipient

        if sender:
            message.name = sender.name
            message.email = sender.email
        message.save()

        return redirect('single_profile',pk=recipient.id)
    context ={
        'recipient':recipient,
        'form':form,
    }

    return render(request,'users/message_form.html',context)

def error401(request):
    return render(request,'401.html')