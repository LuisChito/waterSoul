# ============================================================
#  WATER SOUL — Sistema Experto
#  Archivo: motor_inferencia.py
#  Componente: MOTOR DE INFERENCIA
#
#  Orquesta el ciclo completo del SE:
#    1. Hace preguntas al usuario (llena la base de hechos)
#    2. Aplica encadenamiento hacia adelante (forward chaining)
#    3. Localiza la regla que se dispara
#    4. Invoca el módulo de explicación con el resultado
# ============================================================

from base_hechos        import BaseDeHechos
from base_conocimientos import BaseDeConocimientos
from modulo_explicacion import ModuloExplicacion


class MotorDeInferencia:
    """
    Implementa el ciclo de razonamiento del sistema experto
    mediante encadenamiento hacia adelante (forward chaining):

        Hechos iniciales → aplicar reglas → nueva conclusión

    Actúa como punto de entrada único del sistema.
    """

    # ----------------------------------------------------------
    # Definición de preguntas y sus opciones
    # Cada opción mapea a un valor semántico interno del SE
    # ----------------------------------------------------------
    PREGUNTAS = [
        {
            "criterio": "reaccion",
            "texto":    "¿Cómo enfrentas un reto difícil?",
            "opciones": {
                "1": ("Fluyo sin detenerme",   "rio"),
                "2": ("Mantengo la calma",     "lago"),
                "3": ("Choco con fuerza",      "mar"),
                "4": ("Me adapto al cambio",   "nube"),
            },
        },
        {
            "criterio": "entorno",
            "texto":    "¿Tu lugar ideal para pensar es...?",
            "opciones": {
                "1": ("Con mucha energía y ruido",     "energia"),
                "2": ("En silencio y oscuridad",       "silencio"),
                "3": ("En espacios abiertos y libres", "abierto"),
            },
        },
        {
            "criterio": "percepcion",
            "texto":    "¿Cómo te ven tus amigos?",
            "opciones": {
                "1": ("Alguien profundo y misterioso", "profundo"),
                "2": ("Alguien alegre y transparente", "alegre"),
                "3": ("Alguien fuerte y protector",    "fuerte"),
                "4": ("Alguien activo y movido",       "activo"),
            },
        },
        {
            "criterio": "estilo",
            "texto":    "¿Qué prefieres hacer en tu día libre?",
            "opciones": {
                "1": ("Explorar lo desconocido", "explorar"),
                "2": ("Relajarme al máximo",     "relax"),
                "3": ("Sentir adrenalina pura",  "adrenalina"),
            },
        },
    ]

    # ----------------------------------------------------------
    # Inicialización: inyección de dependencias
    # ----------------------------------------------------------

    def __init__(self):
        self.base_hechos     = BaseDeHechos()
        self.base_conocim    = BaseDeConocimientos()
        self.mod_explicacion = ModuloExplicacion()

    # ----------------------------------------------------------
    # Métodos privados
    # ----------------------------------------------------------

    def _mostrar_banner(self):
        print("\n" + "=" * 54)
        print("   WATER SOUL — Sistema Experto de Personalidad")
        print("=" * 54)
        print("  Responde 4 preguntas para descubrir qué tipo")
        print("  de agua representa tu forma de ser.\n")

    def _hacer_pregunta(self, pregunta: dict) -> str:
        """
        Muestra una pregunta con sus opciones y valida la entrada.

        Returns:
            Valor semántico interno correspondiente a la opción elegida.
        """
        criterio = pregunta["criterio"].upper()
        print(f"\n  [{criterio}] {pregunta['texto']}")
        print("  " + "─" * 44)

        for num, (texto, _) in pregunta["opciones"].items():
            print(f"    {num}. {texto}")

        while True:
            eleccion = input("\n  Tu respuesta: ").strip()
            if eleccion in pregunta["opciones"]:
                return pregunta["opciones"][eleccion][1]   # valor semántico
            print("  ⚠  Opción no válida. Ingresa el número indicado.")

    # ----------------------------------------------------------
    # Ciclo principal (forward chaining)
    # ----------------------------------------------------------

    def ejecutar(self):
        """
        Ciclo completo del SE:
            Paso 1 — Recopilar hechos (preguntas al usuario)
            Paso 2 — Consultar base de conocimientos
            Paso 3 — Activar módulo de explicación
        """
        self._mostrar_banner()

        # ── Paso 1: llenar la base de hechos ──────────────────
        for i, pregunta in enumerate(self.PREGUNTAS, start=1):
            print(f"\n  Pregunta {i} de {len(self.PREGUNTAS)}")
            valor = self._hacer_pregunta(pregunta)
            self.base_hechos.registrar(pregunta["criterio"], valor)

        # ── Paso 2: inferencia (forward chaining) ─────────────
        regla = self.base_conocim.buscar_regla(self.base_hechos.get_todos())

        # ── Paso 3: explicar resultado ─────────────────────────
        if regla:
            self.mod_explicacion.explicar(
                regla["conclusion"],
                self.base_hechos.get_todos(),
            )
        else:
            print("\n  No se encontró un perfil exacto para tu combinación.")
            print("  Verifica que las opciones coincidan con una rama del árbol.\n")

    def nueva_consulta(self):
        """Reinicia la base de hechos y ejecuta una nueva sesión."""
        self.base_hechos.limpiar()
        self.ejecutar()


# ── Punto de entrada ──────────────────────────────────────────
if __name__ == "__main__":
    se = MotorDeInferencia()
    se.ejecutar()

    while True:
        continuar = input("\n  ¿Deseas hacer otra consulta? (s/n): ").strip().lower()
        if continuar == "s":
            se.nueva_consulta()
        else:
            print("\n  ¡Gracias por usar Water Soul! Hasta pronto.\n")
            break
