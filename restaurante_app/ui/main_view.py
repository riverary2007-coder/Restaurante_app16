import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path


class MainView(tk.Frame):
    """Interfaz principal. Los callbacks coordinan y delegan la lógica al servicio."""

    NAVY = "#1F2A44"
    NAVY_2 = "#263653"
    BLUE = "#2D6CDF"
    BLUE_DARK = "#245CC0"
    RED = "#E91E4D"
    WHITE = "#FFFFFF"
    BG = "#F4F7FB"
    TEXT = "#25324B"
    MUTED = "#667085"
    BORDER = "#D8E0EA"

    def __init__(self, master, restaurante_servicio, on_logout, usuario_autenticado=None) -> None:
        super().__init__(master, bg=self.BG)
        self.restaurante_servicio = restaurante_servicio
        self.on_logout = on_logout
        self.usuario_autenticado = usuario_autenticado
        self._imagenes = {}
        self._botones_nav = {}
        self._crear_estilos()
        self._crear_interfaz()
        self._mostrar_pagina("Inicio")

    def _crear_estilos(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(
            "App.Treeview",
            background="white",
            fieldbackground="white",
            foreground=self.TEXT,
            rowheight=30,
            font=("Arial", 10),
        )
        style.configure(
            "App.Treeview.Heading",
            background="#DCE7F7",
            foreground=self.TEXT,
            font=("Arial", 10, "bold"),
            padding=7,
        )
        style.map("App.Treeview", background=[("selected", "#D9E7FF")])
        style.configure(
            "App.TCombobox",
            fieldbackground="white",
            background="white",
            foreground=self.TEXT,
            padding=6,
        )

    def _asset(self, nombre: str):
        ruta = Path(__file__).resolve().parent.parent / "assets" / nombre
        try:
            imagen = tk.PhotoImage(file=str(ruta))
            self._imagenes[nombre] = imagen
            return imagen
        except tk.TclError:
            return None

    def _crear_interfaz(self) -> None:
        self.sidebar = tk.Frame(self, bg=self.NAVY, width=225)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.contenido = tk.Frame(self, bg=self.BG)
        self.contenido.pack(side="left", fill="both", expand=True)

        logo = self._asset("logo_restaurante.png")
        if logo:
            tk.Label(self.sidebar, image=logo, bg=self.NAVY).pack(pady=(22, 12))
        else:
            tk.Label(self.sidebar, text="RESTAURANTE", font=("Arial", 18, "bold"),
                     fg="white", bg=self.NAVY).pack(pady=(28, 12))

        nombre_rol = (f"{self.usuario_autenticado.nombre} · {self.usuario_autenticado.rol}"
                      if self.usuario_autenticado else "Sesión activa")
        tk.Label(self.sidebar, text=nombre_rol, font=("Arial", 10),
                 fg="#C8D4E8", bg=self.NAVY).pack(pady=(0, 24))

        self._crear_boton_nav("Inicio", "icon_home.png")
        if self._es_administrador():
            self._crear_boton_nav("Usuarios", "icon_users.png")
        self._crear_boton_nav("Productos", "icon_products.png")
        self._crear_boton_nav("Ventas", "icon_sales.png")

        tk.Frame(self.sidebar, bg=self.NAVY).pack(fill="both", expand=True)
        self._crear_boton_nav("Cerrar sesión", "icon_logout.png", cerrar=True)

    def _crear_boton_nav(self, texto: str, icono: str, cerrar: bool = False) -> None:
        boton = tk.Button(
            self.sidebar,
            text=f"   {texto}",
            image=self._asset(icono),
            compound="left",
            anchor="w",
            padx=18,
            font=("Arial", 11, "bold"),
            fg="white",
            bg=self.RED if cerrar else self.NAVY_2,
            activebackground=self.RED if cerrar else self.BLUE,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.on_logout if cerrar else lambda t=texto: self._mostrar_pagina(t),
        )
        boton.pack(fill="x", padx=16, pady=5, ipady=9)
        if not cerrar:
            self._botones_nav[texto] = boton

    def _limpiar_contenido(self) -> None:
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def _activar_nav(self, pagina: str) -> None:
        for nombre, boton in self._botones_nav.items():
            boton.configure(bg=self.BLUE if nombre == pagina else self.NAVY_2)

    def _mostrar_pagina(self, pagina: str) -> None:
        if pagina == "Usuarios" and not self._es_administrador():
            messagebox.showwarning("Acceso restringido", "Solo el Administrador puede gestionar usuarios.")
            pagina = "Inicio"
        self._limpiar_contenido()
        self._activar_nav(pagina)
        if pagina == "Inicio":
            self._crear_inicio()
        elif pagina == "Usuarios":
            self._crear_pagina_usuarios()
        elif pagina == "Productos":
            self._crear_pagina_productos()
        elif pagina == "Ventas":
            self._crear_pagina_ventas()

    def _es_administrador(self) -> bool:
        return bool(self.usuario_autenticado and self.usuario_autenticado.rol == "Administrador")

    def _crear_encabezado(self, titulo: str, subtitulo: str = "") -> tk.Frame:
        header = tk.Frame(self.contenido, bg=self.BG)
        header.pack(fill="x", padx=30, pady=(28, 18))
        tk.Label(header, text=titulo, font=("Arial", 24, "bold"),
                 fg=self.TEXT, bg=self.BG).pack(anchor="w")
        if subtitulo:
            tk.Label(header, text=subtitulo, font=("Arial", 10),
                     fg=self.MUTED, bg=self.BG).pack(anchor="w", pady=(5, 0))
        return header

    def _crear_tarjeta(self, parent, titulo: str, valor: str, columna: int) -> None:
        tarjeta = tk.Frame(parent, bg="white", highlightthickness=1,
                           highlightbackground=self.BORDER)
        tarjeta.grid(row=0, column=columna, sticky="nsew", padx=7)
        tk.Label(tarjeta, text=titulo, font=("Arial", 10, "bold"),
                 fg=self.MUTED, bg="white").pack(anchor="w", padx=18, pady=(16, 4))
        tk.Label(tarjeta, text=valor, font=("Arial", 22, "bold"),
                 fg=self.BLUE, bg="white").pack(anchor="w", padx=18, pady=(0, 16))

    def _crear_inicio(self) -> None:
        self._crear_encabezado(
            "Panel principal",
            "Gestión de usuarios, productos y ventas",
        )
        cards = tk.Frame(self.contenido, bg=self.BG)
        cards.pack(fill="x", padx=23)
        for i in range(4):
            cards.columnconfigure(i, weight=1)
        self._crear_tarjeta(cards, "Productos", str(self.restaurante_servicio.cantidad_productos()), 0)
        self._crear_tarjeta(cards, "Usuarios", str(self.restaurante_servicio.cantidad_usuarios()), 1)
        self._crear_tarjeta(cards, "Ventas", str(self.restaurante_servicio.cantidad_ventas()), 2)
        self._crear_tarjeta(cards, "Estado", "Activo", 3)

        info = tk.LabelFrame(
            self.contenido, text="Resumen del sistema",
            font=("Arial", 11, "bold"), fg=self.TEXT, bg="white",
            padx=20, pady=18, bd=1, relief="solid",
        )
        info.pack(fill="both", expand=True, padx=30, pady=24)
        tk.Label(
            info,
            text="Seleccione una sección en el menú lateral para continuar.\n\n"
                 "• Usuarios: consulta de usuarios registrados.\n"
                 "• Productos: registro, consulta, actualización y eliminación.\n"
                 "• Ventas: selección de usuario y producto y registro de la operación.",
            justify="left", anchor="w", font=("Arial", 11),
            fg=self.TEXT, bg="white",
        ).pack(anchor="nw")

    def _crear_tabla(self, parent, columnas, titulos, anchos, altura=14):
        tabla = ttk.Treeview(parent, columns=columnas, show="headings",
                             height=altura, style="App.Treeview")
        for col, titulo, ancho in zip(columnas, titulos, anchos):
            tabla.heading(col, text=titulo)
            tabla.column(col, width=ancho, anchor="center")
        scroll = ttk.Scrollbar(parent, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scroll.set)
        tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        return tabla

    def _crear_pagina_usuarios(self) -> None:
        self._crear_encabezado(
            "Gestión de usuarios",
            "Registre, consulte, actualice y elimine cuentas de Empleado y Cliente",
        )
        zona = tk.Frame(self.contenido, bg=self.BG)
        zona.pack(fill="both", expand=True, padx=30, pady=(0, 25))
        zona.columnconfigure(1, weight=1)
        zona.rowconfigure(0, weight=1)
        formulario = tk.LabelFrame(zona, text="Datos del usuario", font=("Arial", 11, "bold"),
                                   fg=self.TEXT, bg="white", padx=14, pady=12)
        formulario.grid(row=0, column=0, sticky="ns", padx=(0, 16))
        self.campos_usuario = {}
        campos = [("Identificación", "identificacion"), ("Nombre", "nombre"),
                  ("Correo", "correo"), ("Usuario", "usuario"), ("Contraseña", "contrasena")]
        for fila, (etiqueta, clave) in enumerate(campos):
            tk.Label(formulario, text=etiqueta, font=("Arial", 9, "bold"), fg=self.TEXT,
                     bg="white").grid(row=fila, column=0, sticky="w", pady=4)
            entrada = tk.Entry(formulario, width=25, font=("Arial", 10), relief="solid", bd=1,
                               show="*" if clave == "contrasena" else "")
            entrada.grid(row=fila, column=1, padx=(8, 0), pady=4, ipady=4)
            self.campos_usuario[clave] = entrada
        fila_rol = len(campos)
        tk.Label(formulario, text="Rol", font=("Arial", 9, "bold"), fg=self.TEXT,
                 bg="white").grid(row=fila_rol, column=0, sticky="w", pady=4)
        self.rol_usuario = ttk.Combobox(formulario, values=("Empleado", "Cliente"),
                                        state="readonly", width=22, style="App.TCombobox")
        self.rol_usuario.grid(row=fila_rol, column=1, padx=(8, 0), pady=4)
        self.rol_usuario.set("Cliente")
        self.rol_usuario.bind("<<ComboboxSelected>>", self._al_cambiar_rol)
        for campo in self.campos_usuario.values():
            campo.bind("<Return>", self._al_presionar_enter)
            campo.bind("<Escape>", self._al_presionar_escape)
        self.rol_usuario.bind("<Return>", self._al_presionar_enter)
        self.rol_usuario.bind("<Escape>", self._al_presionar_escape)
        botones = tk.Frame(formulario, bg="white")
        botones.grid(row=fila_rol + 1, column=0, columnspan=2, sticky="ew", pady=(12, 0))
        for texto, color, comando in [
            ("＋ Registrar", self.BLUE, self.registrar_usuario),
            ("✎ Actualizar", self.BLUE, self.actualizar_usuario),
            ("▣ Eliminar", self.RED, self.eliminar_usuario),
            ("⌫ Limpiar", self.NAVY, self.limpiar_usuario),
        ]:
            tk.Button(botones, text=texto, command=comando, font=("Arial", 9, "bold"),
                      fg="white", bg=color, activebackground=color, activeforeground="white",
                      relief="flat", cursor="hand2", bd=0).pack(fill="x", pady=3, ipady=5)
        marco = tk.LabelFrame(zona, text="Usuarios registrados", font=("Arial", 11, "bold"),
                              fg=self.TEXT, bg="white", padx=10, pady=10)
        marco.grid(row=0, column=1, sticky="nsew")
        self.tabla_usuarios = self._crear_tabla(
            marco,
            ("identificacion", "nombre", "usuario", "rol"),
            ("Identificación", "Nombre", "Usuario", "Rol"),
            (130, 190, 130, 110),
        )
        self.tabla_usuarios.bind("<<TreeviewSelect>>", self._al_seleccionar_usuario)
        self.tabla_usuarios.bind("<Escape>", self._al_presionar_escape)
        self._usuario_seleccionado_id = None
        self._actualizar_usuarios()

    def _al_cambiar_rol(self, _evento=None) -> None:
        """El rol se limita a Empleado o Cliente en el formulario administrativo."""
        if self.rol_usuario.get() not in ("Empleado", "Cliente"):
            self.rol_usuario.set("Cliente")

    def _al_presionar_enter(self, _evento=None):
        self.registrar_usuario()
        return "break"

    def _al_presionar_escape(self, _evento=None):
        self.limpiar_usuario()
        return "break"

    def _al_seleccionar_usuario(self, _evento=None) -> None:
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return
        valores = self.tabla_usuarios.item(seleccion[0], "values")
        usuario = self.restaurante_servicio.buscar_usuario_por_identificacion(str(valores[0]))
        if usuario is None:
            return
        self._usuario_seleccionado_id = usuario.identificacion
        for clave, valor in (("identificacion", usuario.identificacion), ("nombre", usuario.nombre),
                             ("correo", usuario.correo), ("usuario", usuario.usuario),
                             ("contrasena", usuario.contrasena)):
            entrada = self.campos_usuario[clave]
            entrada.delete(0, tk.END)
            entrada.insert(0, valor)
        self.campos_usuario["identificacion"].configure(state="disabled")
        self.rol_usuario.set(usuario.rol if usuario.rol in ("Empleado", "Cliente") else "Cliente")

    def _leer_usuario_formulario(self):
        return tuple(self.campos_usuario[k].get().strip() for k in
                     ("identificacion", "nombre", "correo", "usuario", "contrasena")) + (self.rol_usuario.get(),)

    def registrar_usuario(self) -> None:
        ok, mensaje = self.restaurante_servicio.registrar_usuario(*self._leer_usuario_formulario())
        if ok:
            self._actualizar_usuarios()
            self.limpiar_usuario()
            self._actualizar_inicio_si_corresponde()
            messagebox.showinfo("Usuarios", mensaje)
        else:
            messagebox.showerror("No se pudo registrar", mensaje)

    def actualizar_usuario(self) -> None:
        if not self._usuario_seleccionado_id:
            messagebox.showwarning("Actualizar", "Seleccione primero un usuario de la tabla.")
            return
        ok, mensaje = self.restaurante_servicio.actualizar_usuario(*self._leer_usuario_formulario())
        if ok:
            self._actualizar_usuarios()
            self.limpiar_usuario()
            messagebox.showinfo("Usuarios", mensaje)
        else:
            messagebox.showerror("No se pudo actualizar", mensaje)

    def eliminar_usuario(self) -> None:
        if not self._usuario_seleccionado_id:
            messagebox.showwarning("Eliminar", "Seleccione primero un usuario de la tabla.")
            return
        nombre = self.campos_usuario["nombre"].get()
        if not messagebox.askyesno("Confirmar eliminación", f"¿Desea eliminar a {nombre}?"):
            return
        ok, mensaje = self.restaurante_servicio.eliminar_usuario(
            self._usuario_seleccionado_id, self.usuario_autenticado.identificacion)
        if ok:
            self._actualizar_usuarios()
            self.limpiar_usuario()
            messagebox.showinfo("Usuarios", mensaje)
        else:
            messagebox.showerror("No se pudo eliminar", mensaje)

    def limpiar_usuario(self) -> None:
        for campo in self.campos_usuario.values():
            campo.configure(state="normal")
            campo.delete(0, tk.END)
        self.rol_usuario.set("Cliente")
        self._usuario_seleccionado_id = None
        if hasattr(self, "tabla_usuarios"):
            self.tabla_usuarios.selection_remove(self.tabla_usuarios.selection())

    def _crear_pagina_productos(self) -> None:
        self._crear_encabezado(
            "Gestión de productos",
            "Registre, consulte, actualice y elimine productos",
        )
        zona = tk.Frame(self.contenido, bg=self.BG)
        zona.pack(fill="both", expand=True, padx=30, pady=(0, 25))
        zona.columnconfigure(1, weight=1)
        zona.rowconfigure(0, weight=1)

        formulario = tk.LabelFrame(
            zona, text="Datos del producto", font=("Arial", 11, "bold"),
            fg=self.TEXT, bg="white", padx=16, pady=16,
        )
        formulario.grid(row=0, column=0, sticky="ns", padx=(0, 18))
        self.entradas = {}
        campos = [("Código", "codigo"), ("Nombre", "nombre"),
                  ("Categoría", "categoria"), ("Precio", "precio"),
                  ("Stock", "stock")]
        for fila, (texto, clave) in enumerate(campos):
            tk.Label(formulario, text=texto, font=("Arial", 10, "bold"),
                     fg=self.TEXT, bg="white").grid(row=fila, column=0,
                     sticky="w", pady=6)
            entrada = tk.Entry(formulario, width=27, font=("Arial", 10),
                               relief="solid", bd=1)
            entrada.grid(row=fila, column=1, padx=(12, 0), pady=6, ipady=5)
            self.entradas[clave] = entrada

        botones = tk.Frame(formulario, bg="white")
        botones.grid(row=len(campos), column=0, columnspan=2, sticky="ew", pady=(15, 0))
        acciones = [
            ("＋  Registrar", self.BLUE, self.registrar_producto),
            ("⌕  Cargar por código", self.NAVY, self.cargar_producto),
            ("✎  Actualizar", self.BLUE, self.actualizar_producto),
            ("▣  Eliminar", self.RED, self.eliminar_producto),
            ("⌫  Limpiar", self.NAVY, self._limpiar_formulario),
        ]
        for texto, color, comando in acciones:
            tk.Button(botones, text=texto, command=comando, font=("Arial", 10, "bold"),
                      fg="white", bg=color, activebackground=color,
                      activeforeground="white", relief="flat", cursor="hand2",
                      bd=0).pack(fill="x", pady=4, ipady=7)

        tabla_marco = tk.LabelFrame(
            zona, text="Productos registrados",
            font=("Arial", 11, "bold"), fg=self.TEXT, bg="white",
            padx=10, pady=10,
        )
        tabla_marco.grid(row=0, column=1, sticky="nsew")
        self.tabla_productos = self._crear_tabla(
            tabla_marco,
            ("codigo", "nombre", "categoria", "precio", "stock"),
            ("Código", "Nombre", "Categoría", "Precio", "Stock"),
            (90, 220, 130, 90, 80),
            altura=14,
        )
        self._actualizar_productos()

    def _crear_pagina_ventas(self) -> None:
        self._crear_encabezado(
            "Gestión de ventas",
            "Seleccione un usuario y un producto para registrar la operación",
        )
        zona = tk.Frame(self.contenido, bg=self.BG)
        zona.pack(fill="both", expand=True, padx=30, pady=(0, 25))
        zona.columnconfigure(1, weight=1)
        zona.rowconfigure(0, weight=1)

        formulario = tk.LabelFrame(
            zona, text="Datos de la venta", font=("Arial", 11, "bold"),
            fg=self.TEXT, bg="white", padx=18, pady=18,
        )
        formulario.grid(row=0, column=0, sticky="ns", padx=(0, 18))

        tk.Label(formulario, text="Usuario", font=("Arial", 10, "bold"),
                 fg=self.TEXT, bg="white").pack(anchor="w", pady=(0, 6))
        self.venta_usuario = ttk.Combobox(formulario, state="readonly",
                                          width=28, style="App.TCombobox")
        self.venta_usuario.pack(fill="x", pady=(0, 16))

        tk.Label(formulario, text="Producto", font=("Arial", 10, "bold"),
                 fg=self.TEXT, bg="white").pack(anchor="w", pady=(0, 6))
        self.venta_producto = ttk.Combobox(formulario, state="readonly",
                                           width=28, style="App.TCombobox")
        self.venta_producto.pack(fill="x", pady=(0, 22))

        tk.Button(
            formulario, text="＋  Registrar venta",
            command=self.registrar_venta,
            font=("Arial", 11, "bold"), fg="white", bg=self.BLUE,
            activebackground=self.BLUE_DARK, activeforeground="white",
            relief="flat", cursor="hand2", bd=0,
        ).pack(fill="x", ipady=10)

        tk.Label(
            formulario,
            text="La acción utiliza command=\ny un callback que delega el\nregistro a RestauranteServicio.",
            font=("Arial", 9), fg=self.MUTED, bg="white",
            justify="left",
        ).pack(anchor="w", pady=(22, 0))

        tabla_marco = tk.LabelFrame(
            zona, text="Ventas registradas",
            font=("Arial", 11, "bold"), fg=self.TEXT, bg="white",
            padx=10, pady=10,
        )
        tabla_marco.grid(row=0, column=1, sticky="nsew")
        self.tabla_ventas = self._crear_tabla(
            tabla_marco,
            ("usuario", "producto", "fecha"),
            ("Usuario", "Producto", "Fecha"),
            (230, 230, 190),
            altura=14,
        )
        self._cargar_opciones_venta()
        self._actualizar_ventas()

    def _leer_formulario_producto(self):
        codigo = self.entradas["codigo"].get().strip()
        nombre = self.entradas["nombre"].get().strip()
        categoria = self.entradas["categoria"].get().strip()
        try:
            precio = float(self.entradas["precio"].get())
            stock = int(self.entradas["stock"].get())
        except ValueError as error:
            raise ValueError("Precio debe ser numérico y stock debe ser entero.") from error
        return codigo, nombre, categoria, precio, stock

    # ---------- PRODUCTOS: callbacks ----------
    def registrar_producto(self) -> None:
        try:
            datos = self._leer_formulario_producto()
        except ValueError as error:
            messagebox.showwarning("Datos inválidos", str(error))
            return
        ok, mensaje = self.restaurante_servicio.registrar_producto(*datos)
        if ok:
            self._actualizar_productos()
            self._limpiar_formulario()
            messagebox.showinfo("Producto", mensaje)
        else:
            messagebox.showerror("No se pudo registrar", mensaje)

    def cargar_producto(self) -> None:
        codigo = self.entradas["codigo"].get().strip()
        if not codigo:
            messagebox.showwarning("Consulta", "Ingrese el código del producto.")
            return
        producto = self.restaurante_servicio.cargar_producto(codigo)
        if producto is None:
            messagebox.showerror("Consulta", "Producto no encontrado.")
            return
        self.entradas["nombre"].delete(0, tk.END)
        self.entradas["nombre"].insert(0, producto.nombre)
        self.entradas["categoria"].delete(0, tk.END)
        self.entradas["categoria"].insert(0, producto.categoria)
        self.entradas["precio"].delete(0, tk.END)
        self.entradas["precio"].insert(0, str(producto.precio))
        self.entradas["stock"].delete(0, tk.END)
        self.entradas["stock"].insert(0, str(producto.stock))
        messagebox.showinfo("Consulta", "Producto cargado correctamente.")

    def actualizar_producto(self) -> None:
        try:
            datos = self._leer_formulario_producto()
        except ValueError as error:
            messagebox.showwarning("Datos inválidos", str(error))
            return
        ok, mensaje = self.restaurante_servicio.actualizar_producto(*datos)
        if ok:
            self._actualizar_productos()
            messagebox.showinfo("Producto", mensaje)
        else:
            messagebox.showerror("No se pudo actualizar", mensaje)

    def eliminar_producto(self) -> None:
        codigo = self.entradas["codigo"].get().strip()
        if not codigo:
            messagebox.showwarning("Eliminar", "Ingrese el código del producto.")
            return
        if not messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Desea eliminar el producto {codigo}?",
        ):
            return
        ok, mensaje = self.restaurante_servicio.eliminar_producto(codigo)
        if ok:
            self._actualizar_productos()
            self._limpiar_formulario()
            messagebox.showinfo("Producto", mensaje)
        else:
            messagebox.showerror("No se pudo eliminar", mensaje)

    def _actualizar_productos(self) -> None:
        if not hasattr(self, "tabla_productos"):
            return
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)
        for producto in self.restaurante_servicio.listar_productos():
            self.tabla_productos.insert(
                "", tk.END,
                values=(
                    producto.codigo,
                    producto.nombre,
                    producto.categoria,
                    f"${producto.precio:.2f}",
                    producto.stock,
                ),
            )

    def _limpiar_formulario(self) -> None:
        if hasattr(self, "entradas"):
            for entrada in self.entradas.values():
                entrada.delete(0, tk.END)

    # ---------- USUARIOS ----------
    def _actualizar_usuarios(self) -> None:
        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)
        for usuario in self.restaurante_servicio.listar_usuarios():
            # El panel permite administrar cuentas de Empleado y Cliente.
            if usuario.rol == "Administrador":
                continue
            self.tabla_usuarios.insert(
                "", tk.END,
                values=(
                    usuario.identificacion,
                    usuario.nombre,
                    usuario.usuario,
                    usuario.rol,
                ),
            )

    # ---------- VENTAS: callback ----------
    def _cargar_opciones_venta(self) -> None:
        usuarios = self.restaurante_servicio.listar_usuarios()
        productos = self.restaurante_servicio.listar_productos()

        self._usuarios_venta = {
            f"{u.nombre} — {u.identificacion}": u.identificacion
            for u in usuarios
        }
        self._productos_venta = {
            f"{p.codigo} — {p.nombre}": p.codigo
            for p in productos
        }

        self.venta_usuario["values"] = list(self._usuarios_venta.keys())
        self.venta_producto["values"] = list(self._productos_venta.keys())

        if self.venta_usuario["values"]:
            self.venta_usuario.current(0)
        if self.venta_producto["values"]:
            self.venta_producto.current(0)

    def registrar_venta(self) -> None:
        usuario_label = self.venta_usuario.get().strip()
        producto_label = self.venta_producto.get().strip()

        if not usuario_label or not producto_label:
            messagebox.showwarning(
                "Datos incompletos",
                "Seleccione un usuario y un producto.",
            )
            return

        identificacion = self._usuarios_venta.get(usuario_label)
        codigo_producto = self._productos_venta.get(producto_label)

        ok, mensaje, _venta = self.restaurante_servicio.registrar_venta(
            identificacion, codigo_producto
        )
        if ok:
            self._actualizar_ventas()
            self._actualizar_inicio_si_corresponde()
            messagebox.showinfo("Venta", mensaje)
        else:
            messagebox.showerror("No se pudo registrar", mensaje)

    def _actualizar_ventas(self) -> None:
        if not hasattr(self, "tabla_ventas"):
            return
        for item in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(item)

        usuarios = {
            u.identificacion: u.nombre
            for u in self.restaurante_servicio.listar_usuarios()
        }
        productos = {
            p.codigo: f"{p.codigo} — {p.nombre}"
            for p in self.restaurante_servicio.listar_productos()
        }

        for venta in self.restaurante_servicio.listar_ventas():
            self.tabla_ventas.insert(
                "", tk.END,
                values=(
                    f"{usuarios.get(venta.usuario_id, venta.usuario_id)}",
                    productos.get(venta.producto_codigo, venta.producto_codigo),
                    venta.fecha,
                ),
            )

    def _actualizar_inicio_si_corresponde(self) -> None:
        # El panel se reconstruye al entrar a Inicio, por lo que no requiere
        # manipular directamente otra vista.
        pass

    def _cerrar_sesion(self) -> None:
        self.on_logout()
