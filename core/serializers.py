from datetime import date
from rest_framework import serializers
from .models import Project, Task, Tag

# Cómo se van a serializar los datos de los modelos a JSON y viceversa.
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]  # id = referencia única, name = nombre del tag


class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            "id", "project", "title", "description",
            "priority", "status", "due_date", "tags", "created_at",
        ]

    # Validación de un solo campo: due_date no puede ser en el pasado
    def validate_due_date(self, value):
        if value and value < date.today():
            raise serializers.ValidationError("La fecha límite no puede ser en el pasado.")
        return value

    # Validación que cruza varios campos
    def validate(self, data):
        if data.get("status") == "completada" and not data.get("due_date"):
            raise serializers.ValidationError(
                "No se puede marcar una tarea como completada sin fecha límite registrada."
            )
        
        project = data.get("project")  
        # Obtiene el proyecto al que pertenece la tarea que estamos validando.

        if project and data.get("status") == "en_progreso":  
        # Solo aplica la regla si la tarea está en progreso y tiene un proyecto asociado.

            has_completed = Task.objects.filter(project=project, status="completada").exists()  
            # Consulta al ORM: busca si existe al menos una tarea con ese proyecto y status="completada".

            if not has_completed:  
                # Si no existe ninguna tarea completada en ese proyecto → error.
                raise serializers.ValidationError(
                    "No se puede poner una tarea en progreso si el proyecto no tiene ninguna tarea completada."
                )

                
        return data


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "tasks", "created_at"]

