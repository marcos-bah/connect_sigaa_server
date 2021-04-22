from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .web_scraping import ScrapingSigaa

#classe que faz as query e serializa os dados
class UserDataViewSet(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = ScrapingSigaa(userlogin=request.data["userlogin"],userpass= request.data["userpass"])
            try:
                response = user.getDataUser()
            except:
                response = {"code": 101, "description": "Erro na coleta dos dados"}
        except:
            response = {"code": 100, "description": "Erro nas credenciais", "help": "Use: {'"'userlogin'"':'"'cpf-sigaa'"','"'userpass'"':'"'senha-sigaa'"'}"}
        return Response(response)

class UserTasksViewSet(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = ScrapingSigaa(userlogin=request.data["userlogin"],userpass= request.data["userpass"])
            try:
                response = user.getTasks()
            except:
                response = {"code": 101, "description": "Erro na coleta dos dados"}
        except:
            response = {"code": 100, "description": "Erro nas credenciais", "help": "Use: {'"'userlogin'"':'"'cpf-sigaa'"','"'userpass'"':'"'senha-sigaa'"'}"}
        return Response(response)

class UserClassesViewSet(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = ScrapingSigaa(userlogin=request.data["userlogin"],userpass= request.data["userpass"])
            try:
                response = user.getClasses()
            except:
                response = {"code": 101, "description": "Erro na coleta dos dados"}
        except:
            response = {"code": 100, "description": "Erro nas credenciais", "help": "Use: {'"'userlogin'"':'"'cpf-sigaa'"','"'userpass'"':'"'senha-sigaa'"'}"}
        return Response(response)

class UserAllViewSet(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = ScrapingSigaa(userlogin=request.data["userlogin"],userpass= request.data["userpass"])
            try:
                response = user.getAll()
            except:
                response = {"code": 101, "description": "Erro na coleta dos dados"}
        except:
            response = {"code": 100, "description": "Erro nas credenciais", "help": "Use: {'"'userlogin'"':'"'cpf-sigaa'"','"'userpass'"':'"'senha-sigaa'"'}"}
        return Response(response)

class UserLastClassesViewSet(APIView):
    #permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        try:
            user = ScrapingSigaa(userlogin=request.data["userlogin"],userpass= request.data["userpass"])
            try:
                response = user.getLastClasses()
            except:
                response = {"code": 101, "description": "Erro na coleta dos dados"}
        except:
            response = {"code": 100, "description": "Erro nas credenciais", "help": "Use: {'"'userlogin'"':'"'cpf-sigaa'"','"'userpass'"':'"'senha-sigaa'"'}"}
        return Response(response)

    