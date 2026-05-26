# ============================================================
#  WATER SOUL — Sistema Experto
#  Archivo: modulo_imagenes.py
#  Componente: MÓDULO DE IMÁGENES
#
#  Carga imágenes locales desde la carpeta /imgs.
#  Usa Pillow (PIL) para procesar y redimensionar.
# ============================================================

import os
import io
import urllib.request
from PIL import Image, ImageTk, ImageDraw

# Ruta base de imágenes locales (relativa a este archivo)
_BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imgs")

# Mapeo tipo → archivo local
IMAGENES_LOCAL = {
    "LAGUNA": os.path.join(_BASE, "Laguna_Bacalar.png"),
    "PLAYA":  os.path.join(_BASE, "Playa_Nazare.png"),
}

# Colores de gradiente de respaldo para tipos sin imagen local
COLORES_RESPALDO = {
    "RÍO":    ("#2D6A4F", "#40916C"),
    "GÉISER": ("#8338EC", "#FF006E"),
}

_cache: dict = {}


def _crear_gradiente(color1: str, color2: str, ancho: int, alto: int) -> Image.Image:
    """Crea una imagen de gradiente vertical entre dos colores hex."""
    img  = Image.new("RGB", (ancho, alto))
    draw = ImageDraw.Draw(img)
    r1, g1, b1 = int(color1[1:3],16), int(color1[3:5],16), int(color1[5:7],16)
    r2, g2, b2 = int(color2[1:3],16), int(color2[3:5],16), int(color2[5:7],16)
    for y in range(alto):
        t = y / alto
        r = int(r1*(1-t) + r2*t)
        g = int(g1*(1-t) + g2*t)
        b = int(b1*(1-t) + b2*t)
        draw.line([(0, y), (ancho, y)], fill=(r, g, b))
    return img


def _recortar_centrado(img: Image.Image, ancho: int, alto: int) -> Image.Image:
    """Redimensiona y recorta centrado al tamaño exacto."""
    img_ratio    = img.width / img.height
    target_ratio = ancho / alto

    if img_ratio > target_ratio:
        new_h = alto
        new_w = int(alto * img_ratio)
    else:
        new_w = ancho
        new_h = int(ancho / img_ratio)

    img  = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - ancho) // 2
    top  = (new_h - alto)  // 2
    return img.crop((left, top, left + ancho, top + alto))


def obtener_imagen_tk(tipo: str, ancho: int = 480, alto: int = 220, url: str | None = None) -> ImageTk.PhotoImage:
    """
    Retorna un PhotoImage listo para usar en tkinter.
    Prioridad: imagen local → gradiente de respaldo.
    """
    key = (tipo, ancho, alto, url)
    if key in _cache:
        return _cache[key]
    img = None

    # 1) Si se proporciona una URL, intentar descargarla
    if url and isinstance(url, str) and url.lower().startswith("http"):
        try:
            with urllib.request.urlopen(url, timeout=8) as resp:
                data = resp.read()
            img = Image.open(io.BytesIO(data)).convert("RGB")
        except Exception:
            img = None

    # 2) Si no hay imagen remota, buscar imagen local por tipo
    if img is None:
        ruta = IMAGENES_LOCAL.get(tipo)
        if ruta and os.path.exists(ruta):
            img = Image.open(ruta).convert("RGB")

    # 3) Si no hay ninguna imagen, crear gradiente de respaldo
    if img is None:
        c1, c2 = COLORES_RESPALDO.get(tipo, ("#378ADD", "#0C447C"))
        img = _crear_gradiente(c1, c2, ancho, alto)

    img   = _recortar_centrado(img, ancho, alto)
    photo = ImageTk.PhotoImage(img)
    _cache[key] = photo
    return photo


def limpiar_cache():
    """Limpia el caché de imágenes."""
    _cache.clear()
