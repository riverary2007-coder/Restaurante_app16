import tkinter as tk
from tkinter import messagebox
from pathlib import Path


class LoginView(tk.Frame):
    """Pantalla de acceso con identidad visual consistente con la aplicación."""

    NAVY = "#1F2A44"
    BLUE = "#2D6CDF"
    LIGHT = "#F4F7FB"
    TEXT = "#25324B"
    GRAY = "#667085"

    def __init__(self, master, restaurante_servicio, on_login_success) -> None:
        super().__init__(master, bg=self.LIGHT)
        self.restaurante_servicio = restaurante_servicio
        self.on_login_success = on_login_success
        self._imagenes = {}
        self._crear_interfaz()

    def _asset(self, nombre: str):
        ruta = Path(__file__).resolve().parent.parent / "assets" / nombre
        try:
            imagen = tk.PhotoImage(file=str(ruta))
            self._imagenes[nombre] = imagen
            return imagen
        except tk.TclError:
            return None

    def _crear_interfaz(self) -> None:
        panel = tk.Frame(self, bg=self.NAVY, width=360)
        panel.pack(side="left", fill="y")
        panel.pack_propagate(False)

        logo = self._asset("logo_restaurante.png")
        if logo:
            tk.Label(panel, image=logo, bg=self.NAVY).pack(pady=(110, 24))
        else:
            tk.Label(panel, text="RESTAURANTE APP", font=("Arial", 25, "bold"),
                     fg="white", bg=self.NAVY).pack(pady=(130, 25))

        tk.Label(panel, text="Gestión de usuarios, productos\ny ventas",
                 font=("Arial", 13), fg="#D9E6FF", bg=self.NAVY,
                 justify="center").pack()

        contenido = tk.Frame(self, bg=self.LIGHT)
        contenido.pack(side="left", fill="both", expand=True)

        tarjeta = tk.Frame(contenido, bg="white", padx=45, pady=40,
                           highlightthickness=1, highlightbackground="#D9E0EA")
        tarjeta.place(relx=0.5, rely=0.5, anchor="center", width=430, height=390)

        tk.Label(tarjeta, text="Bienvenido", font=("Arial", 24, "bold"),
                 fg=self.TEXT, bg="white").pack(pady=(8, 5))
        tk.Label(tarjeta, text="Inicie sesión para continuar",
                 font=("Arial", 11), fg=self.GRAY, bg="white").pack(pady=(0, 28))

        tk.Label(tarjeta, text="Usuario", font=("Arial", 10, "bold"),
                 fg=self.TEXT, bg="white").pack(anchor="w")
        self.usuario_entry = tk.Entry(tarjeta, font=("Arial", 11), relief="solid",
                                      bd=1)
        self.usuario_entry.pack(fill="x", ipady=8, pady=(5, 15))

        tk.Label(tarjeta, text="Contraseña", font=("Arial", 10, "bold"),
                 fg=self.TEXT, bg="white").pack(anchor="w")
        self.contrasena_entry = tk.Entry(tarjeta, font=("Arial", 11), relief="solid",
                                         bd=1, show="*")
        self.contrasena_entry.pack(fill="x", ipady=8, pady=(5, 22))

        tk.Button(tarjeta, text="INGRESAR", font=("Arial", 11, "bold"),
                  fg="white", bg=self.BLUE, activebackground="#245CC0",
                  activeforeground="white", relief="flat", bd=0,
                  cursor="hand2", command=self._ingresar).pack(fill="x", ipady=10)

        tk.Label(tarjeta, text="Acceso simulado para fines académicos",
                 font=("Arial", 9), fg=self.GRAY, bg="white").pack(pady=(18, 0))

        self.usuario_entry.focus_set()
        self.usuario_entry.bind("<Return>", lambda _event: self._ingresar())
        self.contrasena_entry.bind("<Return>", lambda _event: self._ingresar())

    def _ingresar(self) -> None:
        usuario = self.usuario_entry.get().strip()
        contrasena = self.contrasena_entry.get()

        if not usuario or not contrasena:
            messagebox.showwarning("Datos incompletos",
                                   "Ingrese usuario y contraseña.")
            return

        if not self.restaurante_servicio.validar_acceso(usuario, contrasena):
            messagebox.showerror("Acceso denegado",
                                 "Usuario o contraseña incorrectos.")
            self.contrasena_entry.delete(0, tk.END)
            self.contrasena_entry.focus_set()
            return

        self.on_login_success(self.restaurante_servicio.buscar_usuario(usuario))
