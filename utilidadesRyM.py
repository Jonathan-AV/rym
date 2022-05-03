import random
import string

def nombrarNArchivo(nombre_archivo):
    prefijo = "".join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(8))
    return prefijo+"_"+nombre_archivo

def generar_nueva_contra():
    ncontra = "".join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(5))
    return ncontra