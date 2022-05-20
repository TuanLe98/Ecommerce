from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
from django.http import HttpResponse
from django.utils.encoding import force_str
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model

from users.models import Profile,Skill
from users.utils.token import account_activation_token

def paginator_profile(request,profiles,result):
    page = request.GET.get('page')
    paginator = Paginator(profiles,result)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = int(page)-1
    if leftIndex < 1:
        leftIndex =1

    rightIndex = int(page)+2
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages

    customer_range = range(leftIndex,rightIndex)

    return profiles, customer_range

def search_profile(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skill = Skill.objects.filter(name__icontains=search_query)
    profile = Profile.objects.distinct().filter(Q(name__icontains=search_query)|
                                     Q(short_intro__icontains=search_query)|
                                     Q(skill__in=skill)|
                                     Q(bio__icontains=search_query))
    return search_query, profile

def wellcome_email(user):
    subject = 'Wellcome Django Project'
    message = 'I am happy when you are here'
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )

def activate(request,uidb64,token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()
        wellcome_email(user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
