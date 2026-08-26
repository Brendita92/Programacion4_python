from django.shortcuts import render

from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok", "service": "TaskFlow API"})

def estado(request):
    return JsonResponse({"estado": "activo", "mensaje": "El servicio está funcionando"})
