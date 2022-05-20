from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .serializers import ProjectSerializers,ProfileSerializers,TagSerializers,ReviewSerializers
from project.models import Project,Tag,Review
from users.models import Profile

# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET':'/api/projects'},
        {'GET':'/api/projects/id'},
        {'GET':'/api/projects/id/vote'},

        {'GET':'/api/users/token'},
        {'GET':'/api/users/token/refresh'}
    ]

    return Response(routes)

@api_view(['GET'])

def get_Projects(request):
    projects = Project.objects.all()
    serializers = ProjectSerializers(projects,many=True)

    return Response(serializers.data)

@api_view(['GET'])
def get_Project(request, pk):
    project = Project.objects.get(id=pk)
    serializers = ProjectSerializers(project,many=False)

    return Response(serializers.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_Profiles(request):
    profiles = Profile.objects.all()
    serializers = ProfileSerializers(profiles,many=True)

    return Response(serializers.data)

@api_view(['GET'])
def get_Profile(request,pk):
    profile = Profile.objects.get(id=pk)
    serializers = ProfileSerializers(profile,many=False)

    return Response(serializers.data)

@api_view(['GET'])
def get_Tag(request):
    tags = Tag.objects.all()
    serializers = TagSerializers(tags,many=True)

    return Response(serializers.data)

@api_view(['GET'])
def get_Review(request):
    reviews = Review.objects.all()
    serializers = ReviewSerializers(many=True)

    return Response(serializers.data)
