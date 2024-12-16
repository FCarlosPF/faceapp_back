import face_recognition
import numpy as np
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import io
from scipy.spatial.distance import euclidean

def obtener_vector_caracteristicas(imagen: InMemoryUploadedFile):
    # Leer la imagen en un array numpy
    imagen_pil = Image.open(imagen)
    imagen_np = np.array(imagen_pil)

    # Encontrar las ubicaciones de las caras en la imagen
    ubicaciones_caras = face_recognition.face_locations(imagen_np)

    # Si no se encuentra ninguna cara, devolver None
    if len(ubicaciones_caras) == 0:
        return None

    # Obtener el vector de características faciales (encoding) de la primera cara encontrada
    vector_caracteristicas = face_recognition.face_encodings(imagen_np, known_face_locations=ubicaciones_caras)[0]

    return vector_caracteristicas.tolist()

def comparar_caracteristicas(vector1, vector2, umbral=0.4):
    """
    Compara dos vectores de características faciales y devuelve True si son similares.
    
    :param vector1: Primer vector de características faciales.
    :param vector2: Segundo vector de características faciales.
    :param umbral: Umbral de similitud. Cuanto menor sea el valor, más estricta será la comparación.
    :return: True si los vectores son similares, False en caso contrario.
    """
    distancia = euclidean(vector1, vector2)
    return distancia <= umbral