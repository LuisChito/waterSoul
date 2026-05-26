# ============================================================
#  WATER SOUL — Sistema Experto
#  Archivo: base_conocimientos.py
#  Componente: BASE DE CONOCIMIENTOS
#
#  Contiene las reglas IF → THEN que representan el
#  conocimiento experto del sistema (árbol de decisión).
# ============================================================

import copy
import json
import os
import hashlib


class BaseDeConocimientos:
    """
    Repositorio de reglas de producción del sistema experto.

    Cada regla tiene la forma:
        IF  (reaccion = X  AND  entorno = Y
             AND  percepcion = Z  AND  estilo = W)
        THEN conclusión

    Las 4 ramas corresponden a los 4 destinos acuáticos del
    árbol de decisión definido en el diseño del SE.
    """

    RUTA_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "arbol_conocimiento.json")

    def __init__(self):
        self._datos = self._cargar_datos()
        self.reglas = self._datos.get("reglas", copy.deepcopy(self._reglas_predeterminadas()))
        self.textos = self._datos.get("textos", {})
        self.ultima_ruta = []

    def _reglas_predeterminadas(self) -> list:
        return [

            # ── RAMA 1 ─────────────────────────────────────────
            {
                "id": "RAMA_1",
                "condiciones": {
                    "reaccion":   "lago",
                    "entorno":    "abierto",
                    "percepcion": "alegre",
                    "estilo":     "relax",
                },
                "conclusion": {
                    "tipo":    "LAGUNA",
                    "esencia": "Reflejo de Paz",
                    "lugar":   "Laguna de Bacalar (Quintana Roo, México)",
                },
            },

            # ── RAMA 2 ─────────────────────────────────────────
            {
                "id": "RAMA_2",
                "condiciones": {
                    "reaccion":   "mar",
                    "entorno":    "abierto",
                    "percepcion": "fuerte",
                    "estilo":     "adrenalina",
                },
                "conclusion": {
                    "tipo":    "PLAYA",
                    "esencia": "Protector Resiliente",
                    "lugar":   "Playa de Nazaré (Portugal)",
                },
            },

            # ── RAMA 3 ─────────────────────────────────────────
            {
                "id": "RAMA_3",
                "condiciones": {
                    "reaccion":   "rio",
                    "entorno":    "silencio",
                    "percepcion": "profundo",
                    "estilo":     "explorar",
                },
                "conclusion": {
                    "tipo":    "RÍO",
                    "esencia": "Explorador Incansable",
                    "lugar":   "Río Secreto (Quintana Roo, México)",
                },
            },

            # ── RAMA 4 ─────────────────────────────────────────
            {
                "id": "RAMA_4",
                "condiciones": {
                    "reaccion":   "nube",
                    "entorno":    "energia",
                    "percepcion": "activo",
                    "estilo":     "explorar",
                },
                "conclusion": {
                    "tipo":    "GÉISER",
                    "esencia": "Espíritu Libre",
                    "lugar":   "Geysers El Tatio (Chile)",
                },
            },
        ]

    # ----------------------------------------------------------
    # Consulta de reglas
    # ----------------------------------------------------------

    def _cargar_datos(self) -> dict:
        if os.path.exists(self.RUTA_DATOS):
            try:
                with open(self.RUTA_DATOS, "r", encoding="utf-8") as archivo:
                    datos = json.load(archivo)
                if isinstance(datos, dict):
                    return datos
            except (OSError, json.JSONDecodeError):
                pass

        datos = {
            "reglas": copy.deepcopy(self._reglas_predeterminadas()),
            "textos": {},
        }
        self._guardar_datos(datos)
        return datos

    def _guardar_datos(self, datos: dict) -> None:
        with open(self.RUTA_DATOS, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)

    def _persistir(self) -> None:
        self._datos = {"reglas": self.reglas, "textos": self.textos}
        self._guardar_datos(self._datos)

    def buscar_regla(self, hechos_dict: dict) -> dict | None:
        """
        Recorre las reglas y retorna la primera cuyas
        condiciones coincidan exactamente con los hechos.

        Args:
            hechos_dict: dict de hechos {criterio: valor}

        Returns:
            dict de la regla disparada, o None si ninguna aplica.
        """
        for regla in self.reglas:
            if regla["condiciones"] == hechos_dict:
                self.ultima_ruta = [hechos_dict.get("reaccion", ""), hechos_dict.get("entorno", ""), hechos_dict.get("percepcion", ""), hechos_dict.get("estilo", "")]
                return regla

        # Si no hay una regla exacta en la base clásica, intentar buscar
        # en la nueva estructura `arbol` del JSON (si existe). El árbol
        # contiene categorías (ej. 'lago','mar','rio','nube') con varias
        # `opciones` (lugares). Seleccionamos una opción determinísticamente
        # a partir de las respuestas del usuario para que la elección sea
        # reproducible entre ejecuciones.
        arbol = self._datos.get("arbol")
        if isinstance(arbol, list):
            reaccion = hechos_dict.get("reaccion")
            if reaccion:
                for nodo in arbol:
                    if nodo.get("id") == reaccion:
                        opciones = nodo.get("opciones", [])
                        if opciones:
                            # Selección determinista por id de opción.
                            # Si el id esperado no existe en el JSON, se
                            # considera ausencia de conocimiento y se retorna None.
                            key_str = "|".join([
                                hechos_dict.get("reaccion", ""),
                                hechos_dict.get("entorno", ""),
                                hechos_dict.get("percepcion", ""),
                                hechos_dict.get("estilo", ""),
                            ])
                            digest = hashlib.sha256(key_str.encode("utf-8")).hexdigest()
                            slot = (int(digest[:16], 16) % 36) + 1
                            opt_id = f"op{slot}"
                            self.ultima_ruta = [
                                hechos_dict.get("reaccion", ""),
                                hechos_dict.get("entorno", ""),
                                hechos_dict.get("percepcion", ""),
                                hechos_dict.get("estilo", ""),
                                opt_id,
                            ]

                            opt = next((opcion for opcion in opciones if opcion.get("id") == opt_id), None)
                            if opt is None:
                                return None

                            conclusion = {
                                "tipo": reaccion.upper(),
                                "respuesta": opt.get("respuesta", ""),
                                "esencia": opt.get("respuesta", ""),
                                "lugar": opt.get("respuesta", ""),
                                "imagen": opt.get("imagen", ""),
                                "explicacion": opt.get("explicacion", ""),
                                "ruta": " > ".join([str(p) for p in self.ultima_ruta if p]),
                            }
                            return {"id": f"ARBO_{reaccion}_{slot}", "conclusion": conclusion}

        return None

    def agregar_regla(self, condiciones: dict, conclusion: dict, regla_id: str | None = None, textos: dict | None = None, ruta: list | None = None) -> dict:
        """
        Agrega una regla nueva al árbol de conocimiento persistente.

        La nueva regla se inserta al inicio para que tenga prioridad
        en consultas posteriores con las mismas condiciones.
        """
        nueva_regla = {
            "id": regla_id or f"REGLA_{len(self.reglas) + 1}",
            "condiciones": dict(condiciones),
            "conclusion": dict(conclusion),
        }
        if ruta:
            nueva_regla["ruta"] = list(ruta)
        self.reglas.insert(0, nueva_regla)
        if textos:
            tipo = conclusion.get("tipo")
            if tipo:
                self.textos[tipo] = dict(textos)
        self._persistir()
        return nueva_regla

    def obtener_textos(self) -> dict:
        """Retorna una copia de los textos persistidos por tipo."""
        return copy.deepcopy(self.textos)

    def obtener_ultima_ruta(self) -> list:
        """Retorna la ultima ruta calculada por el buscador."""
        return list(self.ultima_ruta)

    def listar_reglas(self) -> list:
        """Retorna los IDs de todas las reglas registradas."""
        return [r["id"] for r in self.reglas]

    def __repr__(self):
        return f"BaseDeConocimientos({len(self.reglas)} reglas)"