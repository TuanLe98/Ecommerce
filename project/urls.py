from django.urls import path
from project import views

urlpatterns = [
    path('',views.home,name = 'home'),
    path('create-project/',views.create_project,name='create-project'),
    path('single-project/<str:pk>',views.single_project,name='single-project'),
    path('update-project/<str:pk>',views.update_project,name='update-project'),
    path('delete-project/<str:pk>',views.delete_project,name='delete-project'),
]