# ============================================================
#  WATER SOUL — Sistema Experto
#  Archivo: modulo_explicacion.py
#  Componente: MÓDULO DE EXPLICACIÓN
#
#  Genera la respuesta narrativa que el usuario recibe,
#  incluyendo descripción, recomendación, lugar real y
#  la traza de razonamiento (regla disparada).
# ============================================================


class ModuloExplicacion:
    """
    Responsable de presentar al usuario la conclusión del SE
    de forma comprensible: texto personalizado, recomendación
    y trazabilidad de la inferencia realizada.
    """

    # ----------------------------------------------------------
    # Textos narrativos por tipo de alma (uno por rama)
    # ----------------------------------------------------------
    TEXTOS = {
        "LAGUNA": {
            "recomendacion": (
                "Usa tu claridad mental para ayudar a otros a ver "
                "sus propias verdades. Tu presencia pacífica es un "
                "regalo — compártela con quienes te rodean."
            ),
            "descripcion": (
                "Eres como un cuerpo de agua sereno que invita a la "
                "reflexión. Tu transparencia genera confianza inmediata "
                "y tu calma actúa como un ancla para quienes te rodean. "
                "Sabes que la verdadera fuerza no siempre choca; a veces "
                "simplemente permanece en paz y observa."
            ),
            "dato_lugar": (
                "Famosa por sus siete colores y sus aguas pacíficas "
                "que invitan a la relajación total y la honestidad."
            ),
        },
        "PLAYA": {
            "recomendacion": (
                "Canaliza esa energía desbordante para derribar las "
                "barreras que te impiden avanzar. No le temas al conflicto "
                "cuando es necesario para proteger lo que amas."
            ),
            "descripcion": (
                "Al igual que el océano, posees una fuerza que puede ser "
                "tanto serena como devastadora. Tu personalidad es imponente "
                "y tu presencia llena cualquier espacio; eres ese apoyo "
                "inamovible en el que los demás confían cuando las cosas "
                "se ponen difíciles."
            ),
            "dato_lugar": (
                "Hogar de las olas más grandes y poderosas del mundo, "
                "reflejando tu valentía y tu naturaleza indomable."
            ),
        },
        "RÍO": {
            "recomendacion": (
                "Confía en tu instinto de seguir fluyendo. Cada obstáculo "
                "es solo una curva del camino — rodéalo con elegancia y "
                "sigue avanzando hacia tu destino."
            ),
            "descripcion": (
                "Como un río, nunca te detienes. Tienes una dirección clara "
                "y una energía constante que arrastra todo a su paso. Tu "
                "profundidad y misterio fascinan a quienes te conocen, "
                "aunque pocos logran seguirte el ritmo."
            ),
            "dato_lugar": (
                "Un río subterráneo único en la selva yucateca, que fluye "
                "en la oscuridad revelando sus secretos solo a quienes "
                "se atreven a explorarlo."
            ),
        },
        "GÉISER": {
            "recomendacion": (
                "Aprovecha tus explosiones de energía en momentos clave. "
                "Tu capacidad de transformar presión en potencia es tu "
                "mayor fortaleza — úsala con intención."
            ),
            "descripcion": (
                "Como un géiser, acumulas energía en silencio y la liberas "
                "de forma espectacular. Eres impredecible, apasionado y "
                "absolutamente memorable. Los que te conocen saben que "
                "cuando actúas, lo haces con toda tu fuerza."
            ),
            "dato_lugar": (
                "A más de 4,300 metros de altitud en el desierto de Atacama, "
                "los géiseres brotan cada madrugada con una energía "
                "tan poderosa como la tuya."
            ),
        },
    }

    # ----------------------------------------------------------
    # Métodos de presentación
    # ----------------------------------------------------------

    def explicar(self, conclusion: dict, hechos_dict: dict):
        """
        Imprime en consola la explicación completa del resultado.

        Args:
            conclusion:  dict con tipo, esencia y lugar
            hechos_dict: dict de hechos que dispararon la regla
        """
        tipo   = conclusion["tipo"]
        textos = self.TEXTOS.get(tipo, {})

        sep = "=" * 54

        print(f"\n{sep}")
        print(f"  Tu alma es: {tipo}")
        print(f"  Esencia   : {conclusion['esencia']}")
        print(sep)

        print(f"\n  Recomendación:\n  {textos.get('recomendacion', '')}\n")
        print(f"  Descripción:\n  {textos.get('descripcion', '')}\n")
        print(f"  Lugar real: {conclusion['lugar']}")
        print(f"  {textos.get('dato_lugar', '')}\n")

        print("  ─── Traza de razonamiento ───────────────────────")
        for criterio, valor in hechos_dict.items():
            print(f"  IF {criterio:<12} = {valor!r}")
        print(f"  THEN tipo = {tipo!r}\n")

    def get_texto(self, tipo: str, clave: str) -> str:
        """
        Retorna un texto específico para uso programático
        (ej. desde la interfaz web).

        Args:
            tipo:  clave del tipo de alma (ej. "LAGUNA")
            clave: campo deseado ("descripcion", "recomendacion", etc.)
        """
        return self.TEXTOS.get(tipo, {}).get(clave, "")

    def __repr__(self):
        tipos = list(self.TEXTOS.keys())
        return f"ModuloExplicacion(tipos={tipos})"