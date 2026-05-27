# Flujo del proyecto Water Soul

Este documento resume como funciona el sistema experto, como recorre su arbol de conocimiento y que hace cada modulo.

## Proposito general

Water Soul es un sistema experto de personalidad. Toma las respuestas del usuario, las convierte en hechos, busca una regla compatible en la base de conocimientos y devuelve una conclusion asociada a un tipo de agua.

El proyecto tiene dos formas de ejecucion principales:

1. Interfaz grafica con `interfaz_tk.py`.
2. Ejecucion por consola con `motor_inferencia.py`.

## Flujo general

1. El sistema inicia y crea las dependencias principales: base de hechos, base de conocimientos y modulo de explicacion.
2. Se muestran 4 preguntas al usuario.
3. Cada respuesta se transforma en un valor semantico interno, por ejemplo `lago`, `mar`, `rio` o `nube`.
4. Esos valores se registran en la base de hechos.
5. El motor consulta la base de conocimientos con todos los hechos capturados.
6. Si existe una regla que coincide exactamente, se obtiene la conclusion asociada.
7. El modulo de explicacion presenta el resultado y la traza de razonamiento.
8. En la interfaz grafica, tambien se muestra la imagen y la descripcion asociada al tipo encontrado.

## Algoritmo que utiliza para recorrer el arbol

El recorrido principal no es un recorrido arborescente clasico como DFS o BFS. El sistema usa encadenamiento hacia adelante y comparacion exacta de condiciones.

### Paso 1: captura de hechos

Cada respuesta se guarda en un diccionario de hechos con estas claves:

- `reaccion`
- `entorno`
- `percepcion`
- `estilo`

### Paso 2: busqueda de coincidencia

La funcion `BaseDeConocimientos.buscar_regla()` compara el diccionario de hechos completo contra cada regla guardada.

La regla se dispara solo si todas las condiciones coinciden exactamente.

En terminos simples:

```text
si hechos == condiciones_de_la_regla
    entonces devolver conclusion
```

### Paso 3: resolucion del resultado

Si encuentra una regla clasica, retorna su conclusion.

Si no encuentra coincidencia exacta, tambien puede consultar la estructura `arbol` guardada en `arbol_conocimiento.json`.

En ese caso:

1. Toma la rama correspondiente segun `reaccion`.
2. Calcula de forma determinista una opcion con SHA-256.
3. Usa esa opcion para obtener una respuesta, imagen y explicacion.

Eso significa que el sistema no recorre el arbol de forma aleatoria. El resultado depende siempre de la misma combinacion de hechos.

## Estructura de datos del arbol

El archivo `arbol_conocimiento.json` guarda dos capas de conocimiento:

- `reglas`: reglas IF/THEN tradicionales.
- `arbol`: nodos con ramas y opciones adicionales.

La parte de `reglas` es la que usa el sistema como base principal de inferencia.
La parte de `arbol` funciona como estructura complementaria para generar conclusiones y recursos visuales.

## Modulos del proyecto

### `interfaz_tk.py`

Es la interfaz grafica principal.

Responsabilidades:

- Mostrar las preguntas al usuario.
- Guardar las respuestas en memoria temporal.
- Llamar al motor de conocimiento.
- Renderizar el resultado con estilo visual.
- Mostrar imagen, descripcion y explicacion del tipo encontrado.

### `motor_inferencia.py`

Es la version de consola del sistema.

Responsabilidades:

- Hacer preguntas por terminal.
- Registrar hechos.
- Consultar la base de conocimientos.
- Mostrar la conclusion final.
- Permitir una nueva consulta despues de terminar.

### `base_hechos.py`

Es la memoria de trabajo del sistema.

Responsabilidades:

- Almacenar los valores actuales de las respuestas.
- Validar que los criterios existan.
- Reiniciar los hechos cuando se inicia una nueva consulta.

### `base_conocimientos.py`

Es el repositorio de reglas y arbol de conocimiento.

Responsabilidades:

- Cargar `arbol_conocimiento.json`.
- Buscar reglas compatibles con los hechos.
- Persistir nuevas reglas o textos si el sistema los agrega.
- Guardar la ultima ruta calculada.

### `modulo_explicacion.py`

Es el modulo encargado de comunicar el resultado.

Responsabilidades:

- Imprimir la conclusion.
- Mostrar esencia, recomendacion y lugar real.
- Presentar la traza de razonamiento.

### `modulo_imagenes.py`

Es el modulo de imagenes para la interfaz grafica.

Responsabilidades:

- Cargar una imagen remota si existe una URL.
- Buscar una imagen local por tipo.
- Generar un degradado de respaldo si no hay imagen.
- Convertir la imagen a formato compatible con Tkinter.

### `arbol_conocimiento.json`

No es un modulo, pero es una pieza central del sistema.

Responsabilidades:

- Definir reglas y conclusiones.
- Asociar tipos con respuestas e imagenes.
- Mantener el conocimiento persistente entre ejecuciones.

## Utilidades del proyecto

La carpeta `utils/` contiene scripts de apoyo para mantenimiento de imagenes y datos.

- `enumerate_images.py`: renombra imagenes con una secuencia numerica.
- `update_images.py`: actualiza rutas de imagen en el JSON.
- `download_lago_images.py`: descarga imagenes desde internet para carga inicial o pruebas.

Estos archivos son utiles como herramientas de mantenimiento, pero no forman parte del flujo normal de ejecucion del sistema.

## Resumen tecnico

El proyecto sigue este patron:

1. Captura de hechos.
2. Inferencia por coincidencia exacta.
3. Despliegue de explicacion.
4. Presentacion visual del resultado.

En otras palabras, Water Soul funciona como un sistema experto basado en reglas, con una interfaz grafica y una capa de recursos visuales para enriquecer la respuesta.