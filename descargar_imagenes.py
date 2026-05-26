import json
import os
import requests
from urllib.parse import urlparse
import mimetypes
import time
import re

def download_images_from_json(json_file_path, output_dir):
    """
    Consulta el archivo JSON del árbol de conocimientos, descarga todas las imágenes
    y las guarda en subdirectorios según la sección (lago, mar, rio, nube).
    """
    # Asegurarse de que el directorio de salida exista
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Leer el archivo JSON
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: No se encontro el archivo " + json_file_path)
        return
    except json.JSONDecodeError as e:
        print("Error al decodificar JSON: " + str(e))
        return

    # Contador para estadísticas
    total_imagenes = 0
    descargadas = 0
    errores = 0

    # Headers para evitar el error 403 de Wikimedia
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Recorrer el árbol de conocimientos
    if 'arbol' in data:
        for categoria in data['arbol']:
            seccion_id = categoria.get('id', 'desconocido')
            # Crear subdirectorio para esta sección
            seccion_dir = os.path.join(output_dir, seccion_id)
            if not os.path.exists(seccion_dir):
                os.makedirs(seccion_dir)

            print(f"\nProcesando sección: {seccion_id}")

            if 'opciones' in categoria:
                for opcion in categoria['opciones']:
                    opcion_id = opcion.get('id')
                    imagen_url = opcion.get('imagen')

                    if opcion_id and imagen_url:
                        total_imagenes += 1
                        print("Procesando imagen " + str(total_imagenes) + ": ID=" + opcion_id + " (Sección: " + seccion_id + ")")

                        # Intentar descargar con reintentos para errores 429
                        max_retries = 3
                        retry_delay = 5  # segundos

                        for attempt in range(max_retries):
                            try:
                                # Descargar la imagen con headers apropiados
                                response = requests.get(imagen_url, headers=headers, timeout=30)

                                # Si es un error 429, esperar y reintentar
                                if response.status_code == 429:
                                    if attempt < max_retries - 1:  # No es el último intento
                                        wait_time = retry_delay * (2 ** attempt)  # Backoff exponencial
                                        print(f"  ! Error 429 (Too Many Requests). Esperando {wait_time} segundos antes de reintentar...")
                                        time.sleep(wait_time)
                                        continue
                                    else:
                                        # Último intento fallido, intentar con miniatura si se sugiere en el error
                                        print("  ! Error 429 persistente. Intentando obtener sugerencia de miniatura...")
                                        # Extraer sugerencia de miniatura del mensaje de error si está disponible
                                        thumbnail_url = extract_thumbnail_suggestion(response.text)
                                        if thumbnail_url:
                                            print(f"  * Probando con URL de miniatura: {thumbnail_url}")
                                            response = requests.get(thumbnail_url, headers=headers, timeout=30)
                                            if response.status_code == 200:
                                                print("  * Miniatura descargada exitosamente")
                                            else:
                                                raise requests.exceptions.RequestException(f"Miniatura también falló: {response.status_code}")
                                        else:
                                            raise requests.exceptions.RequestException(f"Error 429 después de {max_retries} intentos")

                                # Para otros códigos de error, lanzar excepción
                                response.raise_for_status()

                                # Si llegamos aquí, la descarga fue exitosa
                                break

                            except requests.exceptions.RequestException as e:
                                if attempt == max_retries - 1:  # Último intento
                                    print("  ! Error al descargar " + imagen_url + ": " + str(e))
                                    errores += 1
                                    # Si falló después de todos los reintentos, no continuar con el procesamiento de esta imagen
                                    break
                                else:
                                    wait_time = retry_delay * (2 ** attempt)
                                    print(f"  ! Intento {attempt + 1} fallido. Reintentando en {wait_time} segundos...")
                                    time.sleep(wait_time)
                            except Exception as e:
                                print("  ! Error inesperado: " + str(e))
                                errores += 1
                                break
                        else:
                            # Este bloque se ejecuta si el bucle for terminó normalmente (sin break por error)
                            # Procesar la imagen descargada
                            try:
                                # Determinar la extensión del archivo
                                # Primero intentar obtenerla de la URL (o URL de miniatura si se usó)
                                parsed_url = urlparse(imagen_url)
                                path = parsed_url.path
                                extension = os.path.splitext(path)[1]

                                # Si no se pudo obtener de la URL, intentar desde Content-Type
                                if not extension:
                                    content_type = response.headers.get('content-type')
                                    if content_type:
                                        extension = mimetypes.guess_extension(content_type.split(';')[0].strip())
                                        if not extension:
                                            extension = '.bin'  # extension generica
                                    else:
                                        extension = '.bin'  # extension generica

                                # Asegurarse de que la extension este en minusculas
                                extension = extension.lower()

                                # Construir el nombre de archivo
                                filename = f"{opcion_id}{extension}"
                                filepath = os.path.join(seccion_dir, filename)

                                # Guardar la imagen
                                with open(filepath, 'wb') as f:
                                    f.write(response.content)

                                print("  * Descargada: " + filename)
                                descargadas += 1

                            except Exception as e:
                                print("  ! Error al guardar la imagen: " + str(e))
                                errores += 1

                        # Añadir un pequeño retraso para evitar rate limiting
                        time.sleep(1.0)  # Aumentado a 1 segundo para ser más amigable con el API
                    else:
                        print("  Advertencia: Opcion faltante ID o URL de imagen: " + str(opcion))

    # Resumen
    print("\n" + "="*50)
    print("RESUMEN DE DESCARGA")
    print("="*50)
    print("Total de imagenes encontradas: " + str(total_imagenes))
    print("Imagenes descargadas exitosamente: " + str(descargadas))
    print("Errores: " + str(errores))
    print("Directorio de salida: " + os.path.abspath(output_dir))

def extract_thumbnail_suggestion(error_text):
    """
    Extrae la sugerencia de URL de miniatura del texto de error de Wikimedia.
    """
    # Buscar patrones como "https://w.wiki/GHai" o similar en el texto de error
    # Los mensajes de error de Wikimedia a veces incluyen sugerencias
    if "https://w.wiki/" in error_text:
        # Extraer la URL corta
        match = re.search(r'(https://w\.wiki/\w+)', error_text)
        if match:
            short_url = match.group(1)
            try:
                # Resolver la URL corta para obtener la URL real de la miniatura
                response = requests.head(short_url, allow_redirects=True, timeout=10)
                if response.status_code == 200:
                    return response.url
            except:
                pass
    return None

if __name__ == "__main__":
    # Ruta del archivo JSON
    json_file = "arbol_conocimiento.json"
    # Directorio de salida
    output_directory = "imgs"

    print("Iniciando descarga de imagenes desde el arbol de conocimientos...")
    print("Archivo JSON: " + json_file)
    print("Directorio de salida: " + output_directory)
    print("-"*50)

    download_images_from_json(json_file, output_directory)