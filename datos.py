from os import path


def cargar_cantidad_libros_colegio(cantidad_colegios: int):
    cantidad = {}
    for i in range(1, cantidad_colegios + 1):
        with open(path.join("datos", "cantidad_libros_colegio", f"cantidad_libros_{i}"), 'a') as datos:
            pass
    pass
