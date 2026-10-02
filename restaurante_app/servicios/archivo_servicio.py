import json
from pathlib import Path


class ArchivoServicio:
    """Responsable de leer y escribir los archivos JSON del proyecto."""

    def __init__(self, carpeta_datos: str | Path) -> None:
        self.carpeta_datos = Path(carpeta_datos)

    def _leer_json(self, nombre: str) -> list[dict]:
        ruta = self.carpeta_datos / nombre
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as error:
            raise ValueError(f"{nombre} contiene JSON inválido.") from error
        except PermissionError as error:
            raise PermissionError(f"No hay permisos para leer {nombre}.") from error
        if not isinstance(datos, list):
            raise ValueError(f"{nombre} debe contener una lista JSON.")
        return datos

    def _guardar_json(self, nombre: str, datos: list[dict]) -> None:
        ruta = self.carpeta_datos / nombre
        try:
            with open(ruta, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=4)
        except PermissionError as error:
            raise PermissionError(f"No hay permisos para escribir {nombre}.") from error

    def cargar_productos(self) -> list[dict]:
        return self._leer_json("productos.json")

    def cargar_usuarios(self) -> list[dict]:
        return self._leer_json("usuarios.json")

    def cargar_ventas(self) -> list[dict]:
        return self._leer_json("ventas.json")

    def guardar_productos(self, productos: list[dict]) -> None:
        self._guardar_json("productos.json", productos)

    def guardar_usuarios(self, usuarios: list[dict]) -> None:
        self._guardar_json("usuarios.json", usuarios)

    def guardar_ventas(self, ventas: list[dict]) -> None:
        self._guardar_json("ventas.json", ventas)
