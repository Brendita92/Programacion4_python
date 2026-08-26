productos = [
    {"nombre": "laptop", "precio" : 1200, "stock": 15},
    {"nombre": "mouse", "precio" : 25, "stock": 5},
    {"nombre": "teclado", "precio" : 75, "stock": 25},
    {"nombre": "monitor", "precio" : 300, "stock": 8},
]

# #esta linea crea una lista vacia para guardar producto
# productos_bajo_stock = []
# #con el for recorremos cada producto de productos
# for producto in productos:
# #se imprime el nombre y el precio del producto 
#     print(f"Producto: {producto['nombre']}, Precio: ${producto['precio']}")
#     #si el stock de ese producto es menor a 10 
#     if producto['stock'] < 10:
#         #se guarda el producto 
#         productos_bajo_stock.append(producto)

# print("\nProductos con bajo stock:")
# print(productos_bajo_stock)

import csv
import json #trabajar con json
from validar_productos import validar_datos


# # def es para definir una funcion con el nombre calcular_promedio_precio que recibe una lista 
def calcular_promedio_precio(lista):
#       # si la lista esta vacia..
        if not lista:
#          # devuelve cero
          return 0
#       #se suma todos los precio sde los productos dentro de la lista 
#       #se gusrad el resultado en total_precio
        total_precio = sum(p['precio'] for p in lista)
    #       #Calcula el promedio dividiendo la suma de precios por la cantidad de productos en la lista
        return total_precio / len(lista)

# precio_promedio = calcular_promedio_precio(productos)
# print(f"\nEl precio promedio de los productos es: ${precio_promedio:.2f}")


# def validar_datos(nombre_archivo): # Define una función llamada validar_datos. Recibe como parámetro el nombre del archivo que queremos validar.
    
# # Valida un archivo JSON, verificando que el formato sea correcto y que los precios sean valores numéricos. 
   
#     try: #Acá ponemos el código que podría generar algún error
#         with open(nombre_archivo, 'r') as archivo_json: #Abre el archivo en modo lectura cuyo nombre recibimos en nombre_archivo.
#             datos = json.load(archivo_json) #Lee el contenido del archivo JSON y lo convierte a estructuras de datos de Python, como listas y diccionarios.
#             # El resultado se guarda en la variable datos
             
#         if not isinstance(datos, list): #Comprueba si datos NO es una lista. isinstance() permite comprobar el tipo de dato.
#             #En este caso esperamos que el JSON contenga una lista.
#             raise ValueError("El archivo no contiene una lista de datos.") #Genera intencionalmente un error de tipo ValueError porque el archivo no tiene la estructura esperada.
             
#         for item in datos: #Recorre uno por uno los productos que están dentro de la lista y cada producto se guarda temporalmente en la variable item
#             if not isinstance(item.get('precio'), (int, float)): # Obtiene el valor de 'precio' del producto.
#                 #Luego comprueba si ese precio es un número. Se acepta int (entero) o float (decimal). Si NO es un número, entra en el if.
#                 raise TypeError(f"El precio del producto '{item.get('nombre')}' no es numérico.") #Genera un error TypeError indicando qué producto, tiene un precio incorrecto.
#                 #item.get('nombre') obtiene el nombre del producto.
                 
#         print("Validación exitosa.") #no encontramos errores por eso mostramos que la validación fue exitosa
#         return datos 
         
#     except FileNotFoundError: # Captura el error que ocurre si el archivo no existe.
#         print(f"Error: El archivo '{nombre_archivo}' no se encontró.") # Muestra un mensaje indicando que no se encontró el archivo.
 
#         return None #Devuelve None para indicar que no se pudieron obtener datos válidos.
#     except json.JSONDecodeError: #Captura el error que ocurre cuando el archivo no tiene un formato JSON válido
#         print("Error: El archivo no tiene un formato JSON válido.") 
#         return None 
#     except (ValueError, TypeError) as e: #Captura los errores ValueError y TypeError que generamos anteriormente con raise. "as e" guarda el mensaje del error en la variable e
#         print(f"Error en la validación de datos: {e}") 
#         return None 
 
# # ----- Bloque 1 y 2: Manipulación de Datos en memoria y CSV -----

productos_desde_csv = []

try:
    with open('datos.csv', mode='r', encoding='utf-8') as archivo_csv:
        lector_diccionario = csv.DictReader(archivo_csv)

        for fila in lector_diccionario:
            fila['id'] = int(fila['id'])
            fila['precio'] = int(fila['precio'])
            fila['stock'] = int(fila['stock'])
            productos_desde_csv.append(fila)

except FileNotFoundError:
    print("Error: El archivo 'datos.csv' no se encontró.")


# ----- Validación del archivo existente -----

print("\n--- Ejecutando el validador ---")
datos_validados = validar_datos('salida.json')

if datos_validados:
    print("Datos validados correctamente:", datos_validados)