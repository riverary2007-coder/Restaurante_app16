import tkinter as tk
from tkinter import messagebox
from pathlib import Path

from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class RestauranteApp(tk.Tk):
    """Ventana única que coordina LoginView y MainView."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Restaurante App")
        self.geometry("1120x680")
        self.minsize(980, 620)

        carpeta_datos = Path(__file__).resolve().parent / "datos"
        archivo_servicio = ArchivoServicio(carpeta_datos)

        try:
            productos = archivo_servicio.cargar_productos()
            usuarios = archivo_servicio.cargar_usuarios()
            ventas = archivo_servicio.cargar_ventas()
        except (ValueError, PermissionError) as error:
            messagebox.showerror("Error de datos", str(error))
            productos, usuarios, ventas = [], [], []

        self.restaurante_servicio = RestauranteServicio(
            productos, usuarios, ventas, archivo_servicio
        )
        self.mostrar_login()

    def _limpiar_vista(self) -> None:
        for widget in self.winfo_children():
            widget.destroy()

    def mostrar_login(self) -> None:
        self._limpiar_vista()
        LoginView(
            self,
            self.restaurante_servicio,
            self._login_correcto,
        ).pack(fill="both", expand=True)

    def mostrar_principal(self) -> None:
        # El login conserva el usuario validado para controlar la sección administrativa.
        self.usuario_autenticado = getattr(self, "_usuario_pendiente", None)
        self._mostrar_principal_con_usuario()

    def _login_correcto(self, usuario) -> None:
        self._usuario_pendiente = usuario
        self.mostrar_principal()

    def _mostrar_principal_con_usuario(self) -> None:
        self._limpiar_vista()
        MainView(
            self,
            self.restaurante_servicio,
            self.mostrar_login,
            self.usuario_autenticado,
        ).pack(fill="both", expand=True)


def main() -> None:
    app = RestauranteApp()
    app.mainloop()


if __name__ == "__main__":
    main()
