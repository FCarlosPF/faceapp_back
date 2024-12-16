# views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Estudiante, CaracteristicasFaciales
from .utils import obtener_vector_caracteristicas, comparar_caracteristicas
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

@csrf_exempt
def registrar_estudiante(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        numero_matricula = request.POST.get('numero_matricula')
        imagen = request.FILES.get('foto')

        if not imagen:
            return JsonResponse({'status': 'error', 'message': 'Imagen no proporcionada'}, status=400)

        # Validación de correo electrónico
        try:
            validate_email(correo)
        except ValidationError:
            return JsonResponse({'status': 'error', 'message': 'Correo electrónico no válido'}, status=400)

        # Obtén el vector de características faciales (si es necesario)
        vector_caracteristicas = obtener_vector_caracteristicas(imagen)

        if vector_caracteristicas is None:
            return JsonResponse({'status': 'error', 'message': 'No se encontró ninguna cara en la imagen'}, status=400)

        try:
            # Crear el estudiante y subir la imagen a S3
            estudiante = Estudiante.objects.create(
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                numero_matricula=numero_matricula,
                foto=imagen  # Esto se sube automáticamente a S3 si está configurado correctamente
            )

            # Crear las características faciales
            CaracteristicasFaciales.objects.create(
                estudiante=estudiante,
                vector_caracteristicas=vector_caracteristicas
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Estudiante registrado',
                'estudiante_id': estudiante.id
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error al registrar al estudiante: {str(e)}'
            }, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@csrf_exempt
def comparar_estudiante(request):
    if request.method == 'POST':
        estudiante_id = request.POST.get('estudiante_id')
        imagen = request.FILES.get('foto')

        if not estudiante_id or not imagen:
            return JsonResponse({'status': 'error', 'message': 'ID del estudiante o imagen no proporcionados'}, status=400)

        try:
            estudiante = Estudiante.objects.get(id=estudiante_id)
        except Estudiante.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Estudiante no encontrado'}, status=404)

        # Obtén el vector de características faciales de la imagen proporcionada
        vector_caracteristicas_nueva = obtener_vector_caracteristicas(imagen)

        if vector_caracteristicas_nueva is None:
            return JsonResponse({'status': 'error', 'message': 'No se encontró ninguna cara en la imagen'}, status=400)

        # Obtén el vector de características faciales del estudiante
        try:
            caracteristicas_estudiante = CaracteristicasFaciales.objects.get(estudiante=estudiante)
        except CaracteristicasFaciales.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Características faciales del estudiante no encontradas'}, status=404)

        # Compara los vectores de características
        es_similar = comparar_caracteristicas(caracteristicas_estudiante.vector_caracteristicas, vector_caracteristicas_nueva)

        return JsonResponse({
            'status': 'success',
            'message': 'Comparación realizada',
            'es_similar': es_similar
        })
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)