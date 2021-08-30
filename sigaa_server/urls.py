from django.urls import  path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', views.main.as_view()),
    path('api/sigaa/userdata', views.UserDataViewSet.as_view()),
    path('api/sigaa/bodyclass', views.UserBodyClassViewSet.as_view()),
    path('api/sigaa/notices', views.UserNoticesViewSet.as_view()),
    path('api/sigaa/tasks', views.UserTasksViewSet.as_view()),
    path('api/sigaa/classes', views.UserClassesViewSet.as_view()),
    path('api/sigaa/all', views.UserAllViewSet.as_view()),
    path('api/sigaa/lastclasses', views.UserLastClassesViewSet.as_view()),
    path('api/unifei/group', views.UnifeiGetGroupsView.as_view()),
]
