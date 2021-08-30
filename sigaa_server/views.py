from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect

from .web_scraping import ScrapingSigaa, getGroup

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

    def get(self, request, *args, **kwargs):
        return Response()   

class main(APIView):
    def get(self, request, *args, **kwargs):
        return redirect("https://github.com/marcos-bah/connect_sigaa_server")

class UserBodyClassViewSet(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = ScrapingSigaa(userlogin=request.data["userlogin"],userpass= request.data["userpass"])
            try:
                response = user.getBodyClass()
            except Exception as e:
                response = {"code": 101, "description": "Erro na coleta dos dados", "error": e, "error": str(e)}
        except Exception as e:
            response = {"code": 100, "description": "Erro nas credenciais", "help": "Use: {'"'userlogin'"':'"'cpf-sigaa'"','"'userpass'"':'"'senha-sigaa'"'}", "error": str(e)}
        return Response(response)  

    def get(self, request, *args, **kwargs):
        return Response()    
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

    def get(self, request, *args, **kwargs):
        return Response()   

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

    def get(self, request, *args, **kwargs):
        return Response()   

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

    def get(self, request, *args, **kwargs):
        return Response()   

class UserClassesWithGroupViewSet(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = ScrapingSigaa(userlogin=request.data["userlogin"],userpass= request.data["userpass"])
            try:
                response = user.getClassesWithGroup()
            except Exception as e:
                response = {"code": 101, "description": "Erro na coleta dos dados", "error": str(e)}
        except Exception as e:
            print(e)
            response = {"code": 100, "description": "Erro nas credenciais", "error": str(e)}
        return Response(response)

    def get(self, request, *args, **kwargs):
        return Response()  

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

    def get(self, request, *args, **kwargs):
        return Response()   

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
    
    def get(self, request, *args, **kwargs):
        return Response()   

class UnifeiGetGroupsView(APIView):
    #permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        try:
            group = getGroup()

            return Response(group.get_group_csv())
        except Exception as e:
            response = { "error": str(e)}
        return Response(response)
    
    def get(self, request, *args, **kwargs):
        try:
            group = getGroup()
            return Response(group.get_group_csv())
        except Exception as e:
            print(e)
            response = { "error": str(e)}
        return Response(response)