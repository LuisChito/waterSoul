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