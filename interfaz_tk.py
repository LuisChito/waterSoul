# ============================================================
#  WATER SOUL — Sistema Experto
#  Archivo: interfaz_tk.py
#  Interfaz gráfica con tkinter + Pillow
# ============================================================

import tkinter as tk
from tkinter import ttk
import threading

from base_hechos        import BaseDeHechos
from base_conocimientos import BaseDeConocimientos
from modulo_explicacion import ModuloExplicacion
from modulo_imagenes    import obtener_imagen_tk, limpiar_cache

# ── Paleta de colores ────────────────────────────────────────
C = {
    "bg":        "#EBF4FD",
    "surface":   "#FFFFFF",
    "border":    "#B5D4F4",
    "blue_400":  "#378ADD",
    "blue_600":  "#185FA5",
    "blue_800":  "#0C447C",
    "blue_900":  "#042C53",
    "blue_50":   "#E6F1FB",
    "text_pri":  "#042C53",
    "text_sec":  "#185FA5",
    "text_mut":  "#378ADD",
    "white":     "#FFFFFF",
    "success":   "#22C55E",
}

FONT_TITLE  = ("Segoe UI", 20, "bold")
FONT_HEAD   = ("Segoe UI", 13, "bold")
FONT_BODY   = ("Segoe UI", 11)
FONT_SMALL  = ("Segoe UI", 9)
FONT_MONO   = ("Courier New", 10)
FONT_CHIP   = ("Segoe UI", 9, "bold")
FONT_BRAND  = ("Segoe UI", 12, "bold")

# ── Preguntas ────────────────────────────────────────────────
PREGUNTAS = [
    {
        "criterio": "reaccion",
        "tag":  "Pregunta 1 — Reacción",
        "text": "¿Cómo enfrentas un reto difícil?",
        "opts": [
            ("A", "Fluyo sin detenerme",   "Como un río constante",    "rio"),
            ("B", "Mantengo la calma",      "Como un lago sereno",      "lago"),
            ("C", "Choco con fuerza",       "Como el mar",              "mar"),
            ("D", "Me adapto al cambio",    "Como una nube",            "nube"),
        ],
    },
    {
        "criterio": "entorno",
        "tag":  "Pregunta 2 — Entorno",
        "text": "¿Tu lugar ideal para pensar es...?",
        "opts": [
            ("A", "Con mucha energía y ruido",      "Ambientes vibrantes",   "energia"),
            ("B", "En silencio y oscuridad",        "Espacios íntimos",      "silencio"),
            ("C", "En espacios abiertos y libres",  "Naturaleza y amplitud", "abierto"),
        ],
    },
    {
        "criterio": "percepcion",
        "tag":  "Pregunta 3 — Percepción",
        "text": "¿Cómo te ven tus amigos?",
        "opts": [
            ("A", "Alguien profundo y misterioso", "Con profundidad interior", "profundo"),
            ("B", "Alguien alegre y transparente", "Claro y genuino",          "alegre"),
            ("C", "Alguien fuerte y protector",    "Un pilar para otros",      "fuerte"),
            ("D", "Alguien activo y movido",       "Siempre en movimiento",    "activo"),
        ],
    },
    {
        "criterio": "estilo",
        "tag":  "Pregunta 4 — Estilo",
        "text": "¿Qué prefieres hacer en tu día libre?",
        "opts": [
            ("A", "Explorar lo desconocido", "Aventura y descubrimiento", "explorar"),
            ("B", "Relajarme al máximo",     "Descanso y paz total",      "relax"),
            ("C", "Sentir adrenalina pura",  "Deportes extremos",         "adrenalina"),
        ],
    },
]


# ── Helpers de widgets ───────────────────────────────────────

def chip(parent, text, fg=None, bg=None, **kw):
    fg  = fg  or C["blue_600"]
    bg  = bg  or C["blue_50"]
    lbl = tk.Label(parent, text=text, font=FONT_CHIP, fg=fg, bg=bg,
                   padx=10, pady=3, **kw)
    return lbl


def divider(parent):
    f = tk.Frame(parent, bg=C["border"], height=1)
    f.pack(fill="x", pady=8)
    return f


def section_label(parent, text):
    lbl = tk.Label(parent, text=text.upper(), font=("Segoe UI", 8, "bold"),
                   fg=C["blue_600"], bg=C["surface"])
    lbl.pack(anchor="w", pady=(6, 3))
    return lbl


def _text_box(parent, text):
    """Caja de texto readonly que hace word-wrap y ajusta su altura automáticamente."""
    box = tk.Text(parent, font=FONT_BODY, fg=C["blue_800"], bg=C["blue_50"],
                  relief="flat", bd=0,
                  wrap="word",
                  padx=12, pady=10,
                  height=4,
                  cursor="arrow",
                  state="normal")
    box.insert("1.0", text)
    box.configure(state="disabled")
    box.pack(fill="x", pady=(0, 6))

    def _auto_height(event=None):
        # Cuenta las líneas VISUALES (word-wrapped), no las lógicas
        n = box.count("1.0", "end", "displaylines")
        if n:
            box.configure(height=n[0])

    box.bind("<Configure>", _auto_height)
    return box


# ── Clase principal ──────────────────────────────────────────

class WaterSoulApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Water Soul — Sistema Experto")
        self.configure(bg=C["bg"])
        self.resizable(False, False)
        self.geometry("560x680")

        # Módulos del SE
        self.base_hechos  = BaseDeHechos()
        self.base_conocim = BaseDeConocimientos()
        self.mod_expl     = ModuloExplicacion()

        # Estado
        self.current   = 0
        self.hechos    = {}
        self.sel_var   = tk.StringVar(value="")
        self._img_ref  = None   # referencia para evitar GC

        # Contenedor principal centrado
        outer = tk.Frame(self, bg=C["bg"])
        outer.pack(expand=True, fill="both", padx=20, pady=20)

        self.card = tk.Frame(outer, bg=C["surface"],
                             highlightbackground=C["border"],
                             highlightthickness=1, bd=0)
        self.card.pack(fill="both", expand=True)

        # Canvas+scrollbar para resultado largo
        self.canvas = tk.Canvas(self.card, bg=C["surface"],
                                highlightthickness=0)
        self.vsb = ttk.Scrollbar(self.card, orient="vertical",
                                 command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.inner = tk.Frame(self.canvas, bg=C["surface"])
        self.canvas_win = self.canvas.create_window(
            (0, 0), window=self.inner, anchor="nw")

        self.inner.bind("<Configure>", self._on_inner_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.canvas.pack(side="left", fill="both", expand=True)

        self._build_quiz()

    # ── Scroll helpers ───────────────────────────────────────

    def _on_inner_configure(self, e):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, e):
        self.canvas.itemconfig(self.canvas_win, width=e.width)

    def _on_mousewheel(self, e):
        self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

    def _clear_inner(self):
        for w in self.inner.winfo_children():
            w.destroy()
        self.canvas.yview_moveto(0)
        self.vsb.pack_forget()

    # ── Brand header ─────────────────────────────────────────

    def _brand(self, parent, subtitle="Sistema experto"):
        row = tk.Frame(parent, bg=C["surface"])
        row.pack(fill="x", pady=(18, 10), padx=22)

        icon = tk.Label(row, text="💧", font=("Segoe UI", 18),
                        bg=C["blue_400"], fg=C["white"],
                        width=2, pady=2)
        icon.pack(side="left")

        tk.Label(row, text="Water Soul", font=FONT_BRAND,
                 fg=C["blue_600"], bg=C["surface"]).pack(side="left", padx=8)

        chip(row, subtitle).pack(side="right")

    # ── Progress bar ─────────────────────────────────────────

    def _progress(self, parent, step, total):
        row = tk.Frame(parent, bg=C["surface"])
        row.pack(fill="x", padx=22, pady=(0, 12))

        bar_bg = tk.Frame(row, bg=C["blue_50"], height=5)
        bar_bg.pack(side="left", fill="x", expand=True)
        bar_bg.pack_propagate(False)

        pct = int((step / total) * 100)
        bar_fill = tk.Frame(bar_bg, bg=C["blue_400"], height=5)
        bar_fill.place(relx=0, rely=0, relwidth=pct / 100, relheight=1)

        tk.Label(row, text=f"{step} de {total}", font=FONT_SMALL,
                 fg=C["blue_600"], bg=C["surface"]).pack(side="right", padx=(8, 0))

    # ── PANTALLA QUIZ ─────────────────────────────────────────

    def _build_quiz(self):
        self._clear_inner()
        self.sel_var.set(self.hechos.get(PREGUNTAS[self.current]["criterio"], ""))

        q = PREGUNTAS[self.current]

        self._brand(self.inner)
        self._progress(self.inner, self.current + 1, len(PREGUNTAS))

        pad = tk.Frame(self.inner, bg=C["surface"])
        pad.pack(fill="x", padx=22)

        chip(pad, q["tag"]).pack(anchor="w", pady=(0, 6))

        tk.Label(pad, text=q["text"], font=FONT_HEAD,
                 fg=C["text_pri"], bg=C["surface"],
                 wraplength=490, justify="left").pack(anchor="w", pady=(0, 12))

        # Opciones
        self._opt_frames = {}
        for ltr, main, hint, val in q["opts"]:
            self._make_option(pad, ltr, main, hint, val, q["criterio"])

        # Navegación
        nav = tk.Frame(self.inner, bg=C["surface"])
        nav.pack(fill="x", padx=22, pady=16)

        if self.current > 0:
            back_btn = tk.Button(nav, text="← Anterior", font=FONT_BODY,
                                 fg=C["blue_600"], bg=C["blue_50"],
                                 activebackground=C["border"],
                                 relief="flat", bd=0, padx=14, pady=7,
                                 cursor="hand2", command=self._prev)
            back_btn.pack(side="left")

        lbl_next = "Ver resultado ✓" if self.current == len(PREGUNTAS) - 1 else "Siguiente →"
        next_btn = tk.Button(nav, text=lbl_next, font=FONT_BODY,
                             fg=C["white"], bg=C["blue_400"],
                             activebackground=C["blue_600"],
                             relief="flat", bd=0, padx=14, pady=7,
                             cursor="hand2", command=self._next)
        next_btn.pack(side="right")

    def _make_option(self, parent, ltr, main, hint, val, criterio):
        sel = self.sel_var.get() == val

        fr = tk.Frame(parent,
                      bg=C["blue_50"] if sel else C["surface"],
                      highlightbackground=C["blue_400"] if sel else C["border"],
                      highlightthickness=1 if sel else 1,
                      cursor="hand2")
        fr.pack(fill="x", pady=4)

        inner = tk.Frame(fr, bg=fr["bg"])
        inner.pack(fill="x", padx=12, pady=10)

        ltr_bg = C["blue_400"] if sel else C["blue_50"]
        ltr_fg = C["white"]    if sel else C["blue_600"]
        ltr_lbl = tk.Label(inner, text=ltr, font=FONT_CHIP,
                           fg=ltr_fg, bg=ltr_bg,
                           width=2, pady=3)
        ltr_lbl.pack(side="left")

        txt_fr = tk.Frame(inner, bg=fr["bg"])
        txt_fr.pack(side="left", padx=10)
        tk.Label(txt_fr, text=main, font=FONT_BODY,
                 fg=C["text_pri"], bg=fr["bg"],
                 anchor="w").pack(anchor="w")
        tk.Label(txt_fr, text=hint, font=FONT_SMALL,
                 fg=C["text_mut"], bg=fr["bg"],
                 anchor="w").pack(anchor="w")

        # Bind click a todos los hijos
        for w in [fr, inner, ltr_lbl, txt_fr] + txt_fr.winfo_children():
            w.bind("<Button-1>", lambda e, v=val, c=criterio: self._select(c, v))

    def _select(self, criterio, val):
        self.hechos[criterio] = val
        self.sel_var.set(val)
        self._build_quiz()

    def _next(self):
        criterio = PREGUNTAS[self.current]["criterio"]
        if criterio not in self.hechos:
            return
        if self.current < len(PREGUNTAS) - 1:
            self.current += 1
            self._build_quiz()
        else:
            self._show_result()

    def _prev(self):
        if self.current > 0:
            self.current -= 1
            self._build_quiz()

    # ── PANTALLA RESULTADO ────────────────────────────────────

    def _show_result(self):
        regla = self.base_conocim.buscar_regla(self.hechos)
        if not regla:
            self._show_no_match()
            return

        self._clear_inner()
        self.vsb.pack(side="right", fill="y")

        conc  = regla["conclusion"]
        tipo  = conc["tipo"]
        textos = self.mod_expl.TEXTOS.get(tipo, {})

        self._brand(self.inner, "Tu resultado")

        pad = tk.Frame(self.inner, bg=C["surface"])
        pad.pack(fill="x", padx=22)

        # Chip "Análisis completado"
        chip(pad, "✓  Análisis completado",
             fg=C["success"], bg="#F0FDF4").pack(anchor="w", pady=(0, 6))

        # Título  ─ "Eres la LAGUNA"
        eres_row = tk.Frame(pad, bg=C["surface"])
        eres_row.pack(anchor="w", pady=(0, 2))
        tk.Label(eres_row, text="Eres la ", font=("Segoe UI", 22),
                 fg=C["blue_600"], bg=C["surface"]).pack(side="left")
        tk.Label(eres_row, text=conc["tipo"], font=("Segoe UI", 26, "bold"),
                 fg=C["blue_800"], bg=C["surface"]).pack(side="left")
        tk.Label(pad, text=f"Tu esencia: {conc['esencia']}", font=FONT_BODY,
                 fg=C["blue_400"], bg=C["surface"]).pack(anchor="w", pady=(0, 10))

        # ── FOTO DEL LUGAR ───────────────────────────────────
        img_frame = tk.Frame(pad, bg=C["blue_400"],
                             highlightbackground=C["border"],
                             highlightthickness=1)
        img_frame.pack(fill="x", pady=(0, 8))

        self._loading_lbl = tk.Label(img_frame, text="Cargando imagen...",
                                     font=FONT_SMALL, fg=C["white"],
                                     bg=C["blue_400"], pady=80)
        self._loading_lbl.pack()

        def load_img():
            photo = obtener_imagen_tk(tipo, ancho=516, alto=210)
            def update():
                self._loading_lbl.destroy()
                img_lbl = tk.Label(img_frame, image=photo, bg=C["blue_400"])
                img_lbl.pack()
                self._img_ref = photo
            self.after(0, update)

        threading.Thread(target=load_img, daemon=True).start()

        # Chip lugar
        chip(pad, f"📍  {conc['lugar']}").pack(anchor="w", pady=(4, 2))

        divider(pad)

        # Dato del lugar
        section_label(pad, "Sobre el lugar")
        _text_box(pad, textos.get("dato_lugar", ""))

        divider(pad)

        # Descripción
        section_label(pad, "Descripción")
        _text_box(pad, textos.get("descripcion", ""))

        divider(pad)

        # Recomendación
        section_label(pad, "Recomendación")
        _text_box(pad, textos.get("recomendacion", ""))

        # Botones
        btn_row = tk.Frame(self.inner, bg=C["surface"])
        btn_row.pack(fill="x", padx=22, pady=16)

        btn_info = tk.Frame(btn_row, bg=C["surface"])
        btn_info.pack(side="left")

        tk.Button(btn_info, text="📄  Base de hechos", font=FONT_BODY,
                  fg=C["blue_600"], bg=C["blue_50"],
                  activebackground=C["border"],
                  relief="flat", bd=0, padx=14, pady=8,
                  cursor="hand2",
                  command=lambda: self._mostrar_detalle(
                      "Base de hechos",
                      self._formatear_base_hechos(),
                  )).pack(side="left", padx=(0, 8))

        tk.Button(btn_info, text="🧠  Base de conocimientos", font=FONT_BODY,
                  fg=C["blue_600"], bg=C["blue_50"],
                  activebackground=C["border"],
                  relief="flat", bd=0, padx=14, pady=8,
                  cursor="hand2",
                  command=lambda: self._mostrar_detalle(
                      "Base de conocimientos",
                      self._formatear_base_conocimientos(regla),
                  )).pack(side="left")

        tk.Button(btn_row, text="🔄  Nueva consulta", font=FONT_BODY,
                  fg=C["white"], bg=C["blue_400"],
                  activebackground=C["blue_600"],
                  relief="flat", bd=0, padx=16, pady=8,
                  cursor="hand2", command=self._restart).pack(side="right")

    def _mostrar_detalle(self, titulo, contenido):
        ventana = tk.Toplevel(self)
        ventana.title(titulo)
        ventana.configure(bg=C["bg"])
        ventana.geometry("620x420")
        ventana.resizable(False, False)

        marco = tk.Frame(ventana, bg=C["surface"], highlightbackground=C["border"],
                         highlightthickness=1)
        marco.pack(fill="both", expand=True, padx=16, pady=16)

        tk.Label(marco, text=titulo, font=FONT_HEAD, fg=C["blue_800"],
                 bg=C["surface"]).pack(anchor="w", padx=16, pady=(16, 8))

        cuerpo = tk.Frame(marco, bg=C["surface"])
        cuerpo.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        texto = tk.Text(cuerpo, font=FONT_BODY, fg=C["blue_800"], bg=C["blue_50"],
                        relief="flat", bd=0, wrap="word", padx=12, pady=12)
        texto.insert("1.0", contenido)
        texto.configure(state="disabled")

        scroll = ttk.Scrollbar(cuerpo, orient="vertical", command=texto.yview)
        texto.configure(yscrollcommand=scroll.set)

        texto.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def _formatear_base_hechos(self):
        etiquetas = {
            "reaccion": "Reacción",
            "entorno": "Entorno",
            "percepcion": "Percepción",
            "estilo": "Estilo",
        }
        lineas = ["Hechos registrados:\n"]
        for criterio, valor in self.hechos.items():
            valor_mostrar = "Sin respuesta" if valor is None else valor
            lineas.append(f"- {etiquetas.get(criterio, criterio.title())}: {valor_mostrar}")
        return "\n".join(lineas)

    def _formatear_base_conocimientos(self, regla_actual):
        lineas = ["Reglas del sistema:\n"]
        for regla in self.base_conocim.reglas:
            condiciones = regla["condiciones"]
            conclusion = regla["conclusion"]
            lineas.append(f"{regla['id']}")
            lineas.append(
                "  IF "
                f"reaccion={condiciones['reaccion']}, "
                f"entorno={condiciones['entorno']}, "
                f"percepcion={condiciones['percepcion']}, "
                f"estilo={condiciones['estilo']}"
            )
            lineas.append(
                "  THEN "
                f"tipo={conclusion['tipo']}, esencia={conclusion['esencia']}, lugar={conclusion['lugar']}"
            )
            if regla_actual and regla["id"] == regla_actual["id"]:
                lineas.append("  -> Esta es la regla que se activó")
            lineas.append("")
        return "\n".join(lineas).strip()

    def _show_no_match(self):
        self._clear_inner()
        self.vsb.pack(side="right", fill="y")
        self._brand(self.inner)
        pad = tk.Frame(self.inner, bg=C["surface"])
        pad.pack(fill="x", padx=22, pady=20)
        tk.Label(pad, text="⚠  Sin coincidencia",
                 font=FONT_HEAD, fg=C["blue_800"],
                 bg=C["surface"]).pack(pady=(10, 6))
        tk.Label(pad, text="No se encontró un perfil exacto para tu combinación.",
                 font=FONT_BODY, fg=C["text_mut"],
                 bg=C["surface"]).pack()
        tk.Label(pad, text="Si quieres, puedes agregar un nuevo conocimiento para esta consulta.",
                 font=FONT_BODY, fg=C["text_sec"],
                 bg=C["surface"], wraplength=480, justify="center").pack(pady=(8, 0))

        btn_row = tk.Frame(pad, bg=C["surface"])
        btn_row.pack(fill="x", pady=18)

        tk.Button(btn_row, text="➕  Agregar conocimiento", font=FONT_BODY,
                  fg=C["white"], bg=C["success"],
                  activebackground="#16A34A",
                  relief="flat", bd=0, padx=14, pady=8,
                  cursor="hand2", command=self._abrir_formulario_conocimiento).pack(side="left")

        tk.Button(btn_row, text="🔄  Nueva consulta", font=FONT_BODY,
                  fg=C["white"], bg=C["blue_400"],
                  activebackground=C["blue_600"],
                  relief="flat", bd=0, padx=14, pady=8,
                  cursor="hand2", command=self._restart).pack(side="right")

    def _abrir_formulario_conocimiento(self):
        ventana = tk.Toplevel(self)
        ventana.title("Agregar conocimiento")
        ventana.configure(bg=C["bg"])
        ventana.geometry("620x560")
        ventana.resizable(False, False)
        ventana.transient(self)
        ventana.grab_set()

        marco = tk.Frame(ventana, bg=C["surface"], highlightbackground=C["border"],
                         highlightthickness=1)
        marco.pack(fill="both", expand=True, padx=16, pady=16)

        encabezado = tk.Frame(marco, bg=C["surface"])
        encabezado.pack(fill="x", padx=16, pady=(16, 8))
        tk.Label(encabezado, text="Regla basada en tus respuestas actuales",
                 font=FONT_HEAD, fg=C["blue_800"], bg=C["surface"]).pack(anchor="w")
        tk.Label(encabezado, text=self._formatear_base_hechos(), font=FONT_SMALL,
                 fg=C["text_mut"], bg=C["surface"], justify="left", wraplength=560).pack(anchor="w", pady=(6, 0))

        body = tk.Frame(marco, bg=C["surface"])
        body.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        tipo_var = tk.StringVar()
        esencia_var = tk.StringVar()
        lugar_var = tk.StringVar()

        def campo_texto(label, variable, row):
            tk.Label(body, text=label, font=FONT_SMALL, fg=C["blue_600"], bg=C["surface"]).grid(
                row=row, column=0, sticky="w", pady=(0, 4)
            )
            entry = tk.Entry(body, textvariable=variable, font=FONT_BODY,
                             fg=C["blue_800"], bg=C["blue_50"], relief="flat")
            entry.grid(row=row + 1, column=0, sticky="ew", pady=(0, 10))
            return entry

        body.columnconfigure(0, weight=1)
        campo_texto("Nombre del nuevo resultado", tipo_var, 0)
        campo_texto("Esencia", esencia_var, 2)
        campo_texto("Lugar", lugar_var, 4)

        def campo_area(label, row):
            tk.Label(body, text=label, font=FONT_SMALL, fg=C["blue_600"], bg=C["surface"]).grid(
                row=row, column=0, sticky="w", pady=(0, 4)
            )
            text = tk.Text(body, height=4, font=FONT_BODY, fg=C["blue_800"], bg=C["blue_50"],
                           relief="flat", bd=0, wrap="word", padx=10, pady=8)
            text.grid(row=row + 1, column=0, sticky="ew", pady=(0, 10))
            return text

        descripcion_txt = campo_area("Descripción", 6)
        recomendacion_txt = campo_area("Recomendación", 8)
        dato_txt = campo_area("Dato del lugar", 10)

        error_lbl = tk.Label(body, text="", font=FONT_SMALL, fg="#B91C1C", bg=C["surface"])
        error_lbl.grid(row=12, column=0, sticky="w", pady=(0, 6))

        btns = tk.Frame(body, bg=C["surface"])
        btns.grid(row=13, column=0, sticky="e", pady=(8, 0))

        def guardar():
            tipo = tipo_var.get().strip().upper()
            esencia = esencia_var.get().strip()
            lugar = lugar_var.get().strip()
            descripcion = descripcion_txt.get("1.0", "end").strip()
            recomendacion = recomendacion_txt.get("1.0", "end").strip()
            dato_lugar = dato_txt.get("1.0", "end").strip()

            if not tipo or not esencia or not lugar:
                error_lbl.config(text="Completa al menos nombre del resultado, esencia y lugar.")
                return

            self.base_conocim.agregar_regla(
                self.hechos,
                {
                    "tipo": tipo,
                    "esencia": esencia,
                    "lugar": lugar,
                },
                regla_id=f"USUARIO_{tipo}",
            )
            self.mod_expl.TEXTOS[tipo] = {
                "descripcion": descripcion,
                "recomendacion": recomendacion,
                "dato_lugar": dato_lugar,
            }
            ventana.destroy()
            self._show_result()

        tk.Button(btns, text="Cancelar", font=FONT_BODY,
                  fg=C["blue_600"], bg=C["blue_50"],
                  relief="flat", bd=0, padx=14, pady=8,
                  cursor="hand2", command=ventana.destroy).pack(side="right", padx=(8, 0))
        tk.Button(btns, text="Guardar conocimiento", font=FONT_BODY,
                  fg=C["white"], bg=C["success"],
                  activebackground="#16A34A",
                  relief="flat", bd=0, padx=14, pady=8,
                  cursor="hand2", command=guardar).pack(side="right")

    def _restart(self):
        self.current = 0
        self.hechos  = {}
        self.sel_var.set("")
        limpiar_cache()
        self._img_ref = None
        self._build_quiz()


# ── Punto de entrada ─────────────────────────────────────────
if __name__ == "__main__":
    app = WaterSoulApp()
    app.mainloop()
