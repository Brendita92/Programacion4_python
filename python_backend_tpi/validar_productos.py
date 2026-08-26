import json

def validar_datos(nombre_archivo): # Define una función llamada validar_datos. Recibe como parámetro el nombre del archivo que queremos validar.
    
# Valida un archivo JSON, verificando que el formato sea correcto y que los precios sean valores numéricos. 
   
    try: #Acá ponemos el código que podría generar algún error
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo_json: #Abre el archivo en modo lectura cuyo nombre recibimos en nombre_archivo.
            datos = json.load(archivo_json) #Lee el contenido del archivo JSON y lo convierte a estructuras de datos de Python, como listas y diccionarios.
            # El resultado se guarda en la variable datos
             
        if not isinstance(datos, list): #Comprueba si datos NO es una lista. isinstance() permite comprobar el tipo de dato.
            #En este caso esperamos que el JSON contenga una lista.
            raise ValueError("El archivo no contiene una lista de datos.") #Genera intencionalmente un error de tipo ValueError porque el archivo no tiene la estructura esperada.
             
        for item in datos: #Recorre uno por uno los productos que están dentro de la lista y cada producto se guarda temporalmente en la variable item
            if not isinstance(item.get('precio'), (int, float)): # Obtiene el valor de 'precio' del producto.
                #Luego comprueba si ese precio es un número. Se acepta int (entero) o float (decimal). Si NO es un número, entra en el if.
                raise TypeError(f"El precio del producto '{item.get('nombre')}' no es numérico.") #Genera un error TypeError indicando qué producto, tiene un precio incorrecto.
                #item.get('nombre') obtiene el nombre del producto.
                 
        print("Validación exitosa.") #no encontramos errores por eso mostramos que la validación fue exitosa
        return datos 
         
    except FileNotFoundError: # Captura el error que ocurre si el archivo no existe.
        print(f"Error: El archivo '{nombre_archivo}' no se encontró.") # Muestra un mensaje indicando que no se encontró el archivo.
 
        return None #Devuelve None para indicar que no se pudieron obtener datos válidos.
    except json.JSONDecodeError: #Captura el error que ocurre cuando el archivo no tiene un formato JSON válido
        print("Error: El archivo no tiene un formato JSON válido.") 
        return None 
    except (ValueError, TypeError) as e: #Captura los errores ValueError y TypeError que generamos anteriormente con raise. "as e" guarda el mensaje del error en la variable e
        print(f"Error en la validación de datos: {e}") 
        return None 
 