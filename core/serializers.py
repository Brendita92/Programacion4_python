from datetime import date 
from .models import Project, Task, Tag
from rest_framework import serializers
from .services import HolidayService
import nh3


# Cómo se van a serializar los datos de los modelos a JSON y viceversa.
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]  # id = referencia única, name = nombre del tag


class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    due_on_holiday = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id", "project", "title", "description", "priority",
            "status", "due_date", "due_on_holiday", "tags", "created_at",
        ]

    def get_due_on_holiday(self, obj):
        if not obj.due_date:
            return False
        return HolidayService.is_holiday(obj.due_date)

    # validate_due_date y validate de la Clase 4 se mantienen igual
    def validate_description(self, value):
        return nh3.clean(value, tags=set())


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "tasks", "created_at"]


