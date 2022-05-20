from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from api import views

urlpatterns = [
    path('', views.getRoutes),
    path('projects/', views.get_Projects),
    path('projects/<str:pk>/', views.get_Project),
    path('profiles/',views.get_Profiles),
    path('profiles/<str:pk>',views.get_Profile),
    path('tags/',views.get_Tag),
    path('reviews/',views.get_Review),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]