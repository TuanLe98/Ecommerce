from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from project.models import Project,Tag

def paginator_project(request,projects,results):

    page = request.GET.get('page')
    paginator = Paginator(projects,results)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    leffIndex = int(page)-1

    if leffIndex < 1:
        leffIndex = 1

    rifghtIndex = int(page)+2

    if rifghtIndex >paginator.num_pages:
        rifghtIndex = paginator.num_pages+1

    customer_range = range(leffIndex,rifghtIndex)
    return projects,customer_range

def search_project(request):
    search_query =''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tag = Tag.objects.filter(name__icontains=search_query)
    project = Project.objects.distinct().filter(Q(title__icontains=search_query)|
                                     Q(owner__name__icontains=search_query)|
                                     Q(tags__in=tag))

    return search_query, project