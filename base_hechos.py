# ============================================================
#  WATER SOUL — Sistema Experto
#  Archivo: base_hechos.py
#  Componente: BASE DE HECHOS
#
#  Almacena dinámicamente las respuestas capturadas del
#  usuario durante una sesión (memoria de trabajo del SE).
# ============================================================


class BaseDeHechos:
    """
    Representa la memoria de trabajo del sistema experto.
    Guarda los valores que el usuario proporciona en cada
    criterio evaluado durante el test.
    """

    # Criterios que el sistema evalúa (orden de preguntas)
    CRITERIOS = ["reaccion", "entorno", "percepcion", "estilo"]

    def __init__(self):
        # Todos los hechos inician como None (sin respuesta)
        self.hechos = {criterio: None for criterio in self.CRITERIOS}

    # ----------------------------------------------------------
    # Operaciones sobre hechos
    # ----------------------------------------------------------

    def registrar(self, criterio: str, valor: str) -> bool:
        """
        Registra un hecho nuevo.

        Args:
            criterio: nombre del criterio (ej. "reaccion")
            valor:    valor semántico elegido (ej. "lago")

        Returns:
            True si el criterio existe y se guardó, False si no.
        """
        if criterio in self.hechos:
            self.hechos[criterio] = valor.lower().strip()
            return True
        return False

    def get(self, criterio: str):
        """Retorna el valor de un hecho o None si no existe."""
        return self.hechos.get(criterio)

    def get_todos(self) -> dict:
        """Retorna una copia del dict completo de hechos."""
        return dict(self.hechos)

    def completo(self) -> bool:
        """True si todos los criterios tienen un valor asignado."""
        return all(v is not None for v in self.hechos.values())

    def limpiar(self):
        """Reinicia todos los hechos (nueva consulta)."""
        for criterio in self.CRITERIOS:
            self.hechos[criterio] = None

    # ----------------------------------------------------------
    # Representación para depuración
    # ----------------------------------------------------------

    def __repr__(self):
        pares = ", ".join(f"{k}={v!r}" for k, v in self.hechos.items())
        return f"BaseDeHechos({pares})"