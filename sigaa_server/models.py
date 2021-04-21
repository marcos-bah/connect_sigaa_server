from django.db import models

#modelo que vai salvar no banco de dados
class Student(models.Model):
    name = models.CharField(max_length=30)
    cpf = models.CharField(max_length=11)

    def __str__(self):
        return self.name
    

   
