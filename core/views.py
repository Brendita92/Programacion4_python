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
#from django.db.migrations import serializer

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
from .services import TaskService, MembershipService
from rest_framework.exceptions import PermissionDenied
from .permissions import IsProjectAdminOrReadOnly
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .serializer_auth import RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Project,ProjectMembership
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
import logging
 
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework_simplejwt.views import TokenObtainPairView
 
from .models import Project, ProjectMembership, SecurityLog
from .throttles import LoginRateThrottle





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
    permission_classes = [
        IsAuthenticated,
        IsProjectAdminOrReadOnly,
    ]

    def get_queryset(self):
        return MembershipService.projects_for(
            self.request.user
        )

    def perform_create(self, serializer):

        with transaction.atomic():

            project = serializer.save()

            ProjectMembership.objects.create(
                project=project,
                user=self.request.user,
                role="admin"
            )


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
    permission_classes = [IsAuthenticated, IsProjectAdminOrReadOnly,]


    def get_queryset(self):
        return super().get_queryset().filter(project__memberships__user=self.request.user).distinct()

    def check_project_admin(self, project):
        if not MembershipService.is_admin(self.request.user,project):
            raise PermissionDenied(
            "Solo un admin del proyecto puede crear o mover tareas en él." )

    def perform_create(self, serializer):
        self.check_project_admin(serializer.validated_data["project"])

        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        if "project" in serializer.validated_data:
            self.check_project_admin(serializer.validated_data["project"]               )

        serializer.save()

        
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

class RegisterView(generics.CreateAPIView):
        queryset = User.objects.all()
        serializer_class = RegisterSerializer
        permission_classes = [permissions.AllowAny]

class SocialLoginJWTView(APIView):
    """
    Después de loguearse con Google, allauth deja al usuario con una sesión
    de Django. Esta vista toma ese usuario y le entrega un par de JWT propios,
    los mismos que devuelve /api/token/ (Clase 6).
    """
 
    def get(self, request):
        refresh = RefreshToken.for_user(request.user)
        return Response({"refresh": str(refresh), "access": str(refresh.access_token)})

security_logger = logging.getLogger("security")
 
 
class ThrottledTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [LoginRateThrottle]
 
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except AuthenticationFailed:
            ip = request.META.get("REMOTE_ADDR")
            username = request.data.get("username", "")
            SecurityLog.objects.create(action="login_failed", detail=f"usuario={username}", ip_address=ip)
            security_logger.warning(f"Login fallido para usuario {username} desde {ip}")
            raise
