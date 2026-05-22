# ============================================================
#  WATER SOUL — Sistema Experto
#  Archivo: base_conocimientos.py
#  Componente: BASE DE CONOCIMIENTOS
#
#  Contiene las reglas IF → THEN que representan el
#  conocimiento experto del sistema (árbol de decisión).
# ============================================================


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

    def __init__(self):
        self.reglas = [

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
                return regla
        return None

    def agregar_regla(self, condiciones: dict, conclusion: dict, regla_id: str | None = None) -> dict:
        """
        Agrega una regla nueva a la base de conocimientos en memoria.

        La nueva regla se inserta al inicio para que tenga prioridad
        en consultas posteriores con las mismas condiciones.
        """
        nueva_regla = {
            "id": regla_id or f"REGLA_{len(self.reglas) + 1}",
            "condiciones": dict(condiciones),
            "conclusion": dict(conclusion),
        }
        self.reglas.insert(0, nueva_regla)
        return nueva_regla

    def listar_reglas(self) -> list:
        """Retorna los IDs de todas las reglas registradas."""
        return [r["id"] for r in self.reglas]

    def __repr__(self):
        return f"BaseDeConocimientos({len(self.reglas)} reglas)"