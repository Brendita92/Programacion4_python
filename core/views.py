# from django.shortcuts import render

# from django.http import JsonResponse

# def health_check(request):
#     return JsonResponse({"status": "ok", "service": "TaskFlow API"})

# def estado(request):
#     return JsonResponse({"estado": "activo", "mensaje": "El servicio está funcionando"})

# from django.http import JsonResponse
# from rest_framework import viewsets
# from .models import Project, Task
# from .serializers import ProjectSerializer, TaskSerializer


# def health_check(request):
#     return JsonResponse({"status": "ok", "service": "TaskFlow API"})


# class ProjectViewSet(viewsets.ModelViewSet):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer


# class TaskViewSet(viewsets.ModelViewSet):
#     queryset = Task.objects.select_related("project").prefetch_related("tags").all()
#     serializer_class = TaskSerializer

# Importa JsonResponse para devolver respuestas simples en formato JSON
from django.http import JsonResponse

# Importa la clase base para crear ViewSets en DRF
from rest_framework import viewsets

# Importa el decorador @action para definir acciones personalizadas en un ViewSet
from rest_framework.decorators import action

# Importa Response para devolver respuestas HTTP con datos serializados
from rest_framework.response import Response

# Importa el modelo Project desde tu aplicación
from .models import Project

# Importa el repositorio de tareas (capa de acceso a datos)
from .repositories import TaskRepository

# Importa los serializers para Project y Task (capa de presentación)
from .serializers import ProjectSerializer, TaskSerializer

# Importa el servicio de tareas (capa de negocio)
from .services import TaskService


# Endpoint simple para verificar que la API está viva
def health_check(request):
    # Devuelve un JSON con estado "ok"
    return JsonResponse({"status": "ok", "service": "TaskFlow API"})


# ViewSet para proyectos (CRUD completo)
class ProjectViewSet(viewsets.ModelViewSet):
    # Define el conjunto de datos que maneja este ViewSet, ordenado por id
    queryset = Project.objects.all().order_by("id")
    # Define el serializer que transforma objetos Project <-> JSON
    serializer_class = ProjectSerializer


# ViewSet para tareas (CRUD completo + acciones personalizadas)
class TaskViewSet(viewsets.ModelViewSet):
    # Usa el repositorio para obtener las tareas optimizadas
    queryset = TaskRepository.get_queryset()
    # Define el serializer que transforma objetos Task <-> JSON
    serializer_class = TaskSerializer

    # Permite filtrar tareas por estos campos en la URL (?status=pendiente, etc.)
    filterset_fields =["id", "title", "created_at", "priority", "project"]

    # Permite ordenar resultados por estos campos (?ordering=due_date, etc.)
    ordering_fields = ["due_date", "created_at", "priority"]

    # Permite buscar tareas por título o descripción (?search=logo, etc.)
    search_fields = ["title", "description"]

    # Acción personalizada: marcar una tarea como completada
    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        # Obtiene la tarea según el ID (pk) de la URL
        task = self.get_object()
        # Llama al servicio para aplicar la regla de negocio (no completar sin due_date)
        TaskService.mark_completed(task)
        # Devuelve la tarea actualizada serializada en la respuesta
        return Response(self.get_serializer(task).data)

    # Acción personalizada: listar tareas vencidas
    @action(detail=False, methods=["get"])
    def overdue(self, request):
        # Usa el servicio para obtener las tareas vencidas
        tasks = TaskService.tasks_overdue(self.get_queryset())
        # Aplica paginación si está configurada en DRF
        page = self.paginate_queryset(tasks)
        if page is not None:
            # Devuelve la respuesta paginada con los datos serializados
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        # Si no hay paginación, devuelve todas las tareas vencidas
        return Response(self.get_serializer(tasks, many=True).data)
