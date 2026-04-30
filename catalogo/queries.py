from __future__ import annotations
from django.db.models import Count, Q, F 
from .models import Autor, Libro, Categoria 

def libros_por_categoria(nombre_categoria: str):
    """
    Retorna un QuerySet de libros filtrados por el nombre de su categoría.
    """
    return Libro.objects.filter(categorias__nombre=nombre_categoria)

def autores_con_mas_de_n_libros(n: int):
    """
    Retorna autores que tienen una cantidad de libros mayor a n.
    Usa annotate para contar la relación inversa con Libro.
    """
    return Autor.objects.annotate(cantidad_libros=Count("libro")).filter(cantidad_libros__gt=n)

def libros_sin_disponibilidad():
    """
    Retorna libros donde la cantidad de préstamos activos iguala al stock total.
    Un préstamo es activo si fecha_devolucion es NULL.
    """
    return Libro.objects.annotate(
        activos=Count("prestamo", filter=Q(prestamo__fecha_devolucion__isnull=True))
    ).filter(activos=F("cantidad_total"))

def top_n_libros_mas_prestados(n: int):
    """
    Retorna los n libros más prestados históricamente, ordenados de mayor a menor.
    """
    return Libro.objects.annotate(total_prestamos=Count("prestamo")).order_by("-total_prestamos")[:n]