from __future__ import annotations
from django.db.models import Count, Q, F 
from .models import Autor, Libro, Categoria 

def libros_por_categoria(nombre_categoria: str):
    return Libro.objects.filter(categorias__nombre=nombre_categoria)


def autores_con_mas_de_n_libros(n: int):
    """
    Devuelve un QuerySet de Autores que tienen más de n libros en el catálogo.
    """
    # 1. Usamos annotate para crear una columna temporal 'cantidad_libros' 
    # 2. Count("libro") cuenta cuántas veces aparece el autor en la tabla Libro
    # 3. filter(cantidad_libros__gt=n) se queda con los que superan el umbral 'n'
    return Autor.objects.annotate(cantidad_libros=Count("libro")).filter(cantidad_libros__gt=n)


def libros_sin_disponibilidad():
    """
    Devuelve un QuerySet de Libros donde no hay copias disponibles.
    (prestamos_activos == cantidad_total)
    """
    # 1. Contamos los préstamos que NO tienen fecha de devolución (activos)
    # 2. Usamos F("cantidad_total") para comparar directamente contra la columna de la tabla
    return Libro.objects.annotate(
        activos=Count("prestamo", filter=Q(prestamo__fecha_devolucion__isnull=True))
    ).filter(activos=F("cantidad_total"))


def top_n_libros_mas_prestados(n: int):
    """
    Devuelve los N libros con más préstamos (historial total).
    """
    # 1. Contamos todos los préstamos asociados a cada libro [cite: 11]
    # 2. Ordenamos de forma descendente (-) por ese conteo [cite: 58]
    # 3. Usamos slicing [:n] para limitar el resultado a los mejores N [cite: 58]
    return Libro.objects.annotate(total_prestamos=Count("prestamo")).order_by("-total_prestamos")[:n]