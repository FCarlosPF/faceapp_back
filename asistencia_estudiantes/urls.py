from django.urls import path
from .views import registrar_estudiante, comparar_estudiante
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('registrar_estudiante/', registrar_estudiante, name='registrar_estudiante'),
    path('comparar_estudiante/', comparar_estudiante, name='comparar_estudiante'),

]

