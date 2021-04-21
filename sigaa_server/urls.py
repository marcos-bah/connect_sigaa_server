from django.urls import  path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('api/sigaa/userdata', views.UserDataViewSet.as_view()),
    path('api/sigaa/tasks', views.UserTasksViewSet.as_view()),
    path('api/sigaa/classes', views.UserClassesViewSet.as_view()),
    path('api/sigaa/all', views.UserAllViewSet.as_view()),
    path('api/sigaa/lastclasses', views.UserLastClassesViewSet.as_view()),

]
