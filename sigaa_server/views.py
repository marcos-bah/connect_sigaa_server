from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect

from .web_scraping import ScrapingSigaa

#classe que faz as query e serializa os dados
class UserDataViewSet(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = ScrapingSigaa(userlogin=request.data["userlogin"],userpass= request.data["userpass"])
            try:
                response = user.getDataUser()
            except Exception as e:
                response = {"code": 101, "description": "Erro na coleta dos dados", "error": str(e)}
        except Exception as e:
            response = {"code": 100, "description": "Erro nas credenciais", "help": "Use: {'"'userlogin'"':'"'cpf-sigaa'"','"'userpass'"':'"'senha-sigaa'"'}", "error": str(e)}
        return Response(response)

class main(APIView):
    def get(self, request, *args, **kwargs):
        return redirect("https://github.com/marcos-bah/connect_sigaa_server")
        
class UserNoticesViewSet(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = ScrapingSigaa(userlogin=request.data["userlogin"],userpass= request.data["userpass"])
            try:
                response = user.getNotices()
            except Exception as e:
                response = {"code": 101, "description": "Erro na coleta dos dados", "error": e, "error": str(e)}
        except Exception as e:
            response = {"code": 100, "description": "Erro nas credenciais", "help": "Use: {'"'userlogin'"':'"'cpf-sigaa'"','"'userpass'"':'"'senha-sigaa'"'}", "error": str(e)}
        return Response(response)

class UserTasksViewSet(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = ScrapingSigaa(userlogin=request.data["userlogin"],userpass= request.data["userpass"])
            try:
                response = user.getTasks()
            except Exception as e:
                response = {"code": 101, "description": "Erro na coleta dos dados", "error": e, "error": str(e)}
        except Exception as e:
            response = {"code": 100, "description": "Erro nas credenciais", "help": "Use: {'"'userlogin'"':'"'cpf-sigaa'"','"'userpass'"':'"'senha-sigaa'"'}", "error": str(e)}
        return Response(response)

class UserClassesViewSet(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = ScrapingSigaa(userlogin=request.data["userlogin"],userpass= request.data["userpass"])
            try:
                response = user.getClasses()
            except Exception as e:
                response = {"code": 101, "description": "Erro na coleta dos dados", "error": str(e)}
        except Exception as e:
            print(e)
            response = {"code": 100, "description": "Erro nas credenciais", "error": str(e)}
        return Response(response)

class UserAllViewSet(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = ScrapingSigaa(userlogin=request.data["userlogin"],userpass= request.data["userpass"])
            try:
                response = user.getAll()
            except Exception as e:
                response = {"code": 101, "description": "Erro na coleta dos dados", "error": str(e)}
        except Exception as e:
            response = {"code": 100, "description": "Erro nas credenciais", "error": str(e)}
        return Response(response)

class UserLastClassesViewSet(APIView):
    #permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        try:
            user = ScrapingSigaa(userlogin=request.data["userlogin"],userpass= request.data["userpass"])
            try:
                response = user.getLastClasses()
            except Exception as e:
                response = {"code": 101, "description": "Erro na coleta dos dados", "error": str(e)}
        except Exception as e:
            response = {"code": 100, "description": "Erro nas credenciais", "help": "Use: {'"'userlogin'"':'"'cpf-sigaa'"','"'userpass'"':'"'senha-sigaa'"'", "error": str(e)}
        return Response(response)

    