#!/usr/bin/env python3
"""
enumerate_images.py
-------------------
Renombra todas las imágenes de una carpeta asignándoles un número secuencial
(1, 2, 3, ...) según el orden en que aparecen al listar el directorio.

Uso:
    python enumerate_images.py /ruta/a/la/carpeta [--ext jpg png] [--dry-run]

- --ext: lista de extensiones a considerar (sin punto). Por defecto: jpg jpeg png gif bmp webp.
- --dry-run: muestra qué cambios se harán sin renombrar realmente.
"""

import argparse
import os
import sys
from pathlib import Path

DEFAULT_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}

def is_image_file(path: Path, exts: set) -> bool:
    return path.suffix.lower() in exts

def main():
    parser = argparse.ArgumentParser(
        description="Renombra imágenes de una carpeta con numeración secuencial."
    )
    parser.add_argument(
        "folder",
        type=str,
        help="Carpeta que contiene las imágenes a renombrar."
    )
    parser.add_argument(
        "--ext",
        nargs="+",
        default=list(DEFAULT_EXTS),
        help="Extensiones de archivo a considerar (ej: jpg png). Sin punto."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Solo muestra las acciones que se realizarían, sin renombrar."
    )
    args = parser.parse_args()

    folder_path = Path(args.folder).expanduser().resolve()
    if not folder_path.is_dir():
        sys.exit(f"Error: '{folder_path}' no es un directorio válido.")

    # Normalizar extensiones (añadir punto y lower)
    exts = {f".{e.lower()}" for e in args.ext}

    # Obtener lista de archivos de imagen en el orden que devuelve el sistema
    all_entries = list(folder_path.iterdir())
    image_files = [p for p in all_entries if p.is_file() and is_image_file(p, exts)]

    if not image_files:
        print("No se encontraron archivos de imagen con las extensiones especificadas.")
        return

    # Ordenar por nombre (puedes cambiar a stat.st_ctime si prefieres orden de creación)
    image_files.sort(key=lambda p: p.name.lower())

    print(f"Se encontraron {len(image_files)} imágenes en '{folder_path}'.\n")
    for idx, src_path in enumerate(image_files, start=1):
        # Mantener la extensión original
        new_name = f"{idx}{src_path.suffix.lower()}"
        dst_path = folder_path / new_name

        if src_path.name == new_name:
            # Ya tiene el nombre correcto; lo saltamos
            continue

        if args.dry_run:
            print(f"[DRY-RUN] {src_path.name}  -->  {new_name}")
        else:
            try:
                src_path.rename(dst_path)
                print(f"Renombrado: {src_path.name}  -->  {new_name}")
            except Exception as e:
                print(f"Error al renombrar '{src_path.name}': {e}")

    if args.dry_run:
        print("\nEjecutó en modo dry-run. No se realizaron cambios reales.")
    else:
        print("\nRenombrado completado.")

if __name__ == "__main__":
    main()