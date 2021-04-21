from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .web_scraping import ScrapingSigaa

#classe que faz as query e serializa os dados
class UserDataViewSet(APIView):
    def post(self, request, *args, **kwargs):
        user = ScrapingSigaa(userlogin=request.data["userlogin"],userpass= request.data["userpass"])
        return Response(user.getDataUser())

class UserTasksViewSet(APIView):
    def post(self, request, *args, **kwargs):
        user = ScrapingSigaa(userlogin=request.data["userlogin"],userpass= request.data["userpass"])
        return Response(user.getTasks())

class UserClassesViewSet(APIView):
    def post(self, request, *args, **kwargs):
        user = ScrapingSigaa(userlogin=request.data["userlogin"],userpass= request.data["userpass"])
        return Response(user.getClasses())

class UserAllViewSet(APIView):
    def post(self, request, *args, **kwargs):
        user = ScrapingSigaa(userlogin=request.data["userlogin"],userpass= request.data["userpass"])
        return Response(user.getAll())

class UserLastClassesViewSet(APIView):
    #permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        user = ScrapingSigaa(userlogin=request.data["userlogin"],userpass= request.data["userpass"])
        return Response(user.getLastClasses())

    