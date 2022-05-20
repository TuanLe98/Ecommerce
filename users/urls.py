from django.urls import path
from users import views

urlpatterns = [
    path('',views.profiles,name='profile'),
    path('login/', views.loginUser, name='login_user'),
    path('register/',views.registerUser,name='register_user'),
    path('logout/',views.logoutUser,name='logout_user'),
    path('delete-user/<str:pk>',views.deleteUser,name='delete_user'),
    path('single-profile/<str:pk>',views.single_profiles,name='single_profile'),
    path('account/',views.account,name='account'),
    path('update-profile/',views.update_profile,name='update_profile'),
    path('create-skill/',views.create_skill,name='create_skill'),
    path('update-skill/<str:pk>',views.update_skill,name='update_skill'),
    path('delete-skill/<str:pk>',views.delete_skill,name='delete_skill'),
    path('inbox/',views.inbox,name='inbox'),
    path('message/<str:pk>',views.message,name='message'),
    path('created-message/<str:pk>',views.created_message,name='created_message'),

    path('401/',views.error401,name='401_error')
]
