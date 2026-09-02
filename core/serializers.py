from rest_framework import serializers
from .models import Project, Task, Tag
 
 #como van a mostrar los datos en la API, es decir,
 #  cómo se van a serializar los datos de los modelos a JSON y viceversa.
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]# id porque estoy haciendo referencia a una instancia de tag en particular, y name porque es el nombre del tag que quiero mostrar en la API.
 
 
class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
 
    class Meta:
        model = Task
        fields = [
            "id", "project", "title", "description",
            "priority", "status", "due_date", "tags", "created_at",
        ]
 
 
class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
 
    class Meta:
        model = Project
        fields = ["id", "name", "description", "tasks", "created_at"]
