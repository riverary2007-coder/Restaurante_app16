from datetime import datetime


class Venta:
    """Modelo de una venta sencilla: usuario, producto y fecha de operación."""

    def __init__(self, usuario_id: str, producto_codigo: str, fecha: str | None = None) -> None:
        self.usuario_id = str(usuario_id).strip()
        self.producto_codigo = str(producto_codigo).strip()
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._validar()

    def _validar(self) -> None:
        if not self.usuario_id:
            raise ValueError("El usuario es obligatorio.")
        if not self.producto_codigo:
            raise ValueError("El producto es obligatorio.")
        if not self.fecha:
            raise ValueError("La fecha es obligatoria.")

    @classmethod
    def from_dict(cls, datos: dict) -> "Venta":
        return cls(
            str(datos["usuario_id"]),
            str(datos["producto_codigo"]),
            str(datos.get("fecha", "")),
        )

    def to_dict(self) -> dict:
        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "fecha": self.fecha,
        }
