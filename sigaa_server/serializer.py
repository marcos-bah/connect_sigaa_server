from django.db.models.fields import Field
from rest_framework import serializers
from sigaa_server.models import Student

#classe com os dados que quero que a api manipule
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'cpf']