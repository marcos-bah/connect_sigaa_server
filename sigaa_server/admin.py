from django.contrib import admin
from sigaa_server.models import Student

#mostra no /admin
class Students(admin.ModelAdmin):
    list_display = ('id', 'name', 'cpf')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

admin.site.register(Student, Students)