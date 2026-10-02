class Usuario:
    """Modelo base de usuario para la simulación de acceso."""

    ROLES = ("Administrador", "Empleado", "Cliente")

    def __init__(self, identificacion: str, nombre: str, correo: str, usuario: str, contrasena: str, rol: str = "Cliente") -> None:
        self.identificacion = identificacion.strip()
        self.nombre = nombre.strip()
        self.correo = correo.strip()
        self.usuario = usuario.strip()
        self.contrasena = contrasena
        self.rol = rol.strip() or "Cliente"

    @classmethod
    def from_dict(cls, datos: dict) -> "Usuario":
        return cls(
            str(datos["identificacion"]),
            str(datos["nombre"]),
            str(datos["correo"]),
            str(datos["usuario"]),
            str(datos["contrasena"]),
            str(datos.get("rol", "Administrador" if str(datos.get("usuario", "")).lower() == "ana" else "Empleado")),
        )

    def __str__(self) -> str:
        return f"{self.identificacion} | {self.nombre} | {self.correo} | {self.rol}"

    def to_dict(self) -> dict:
        return {"identificacion": self.identificacion, "nombre": self.nombre,
                "correo": self.correo, "usuario": self.usuario,
                "contrasena": self.contrasena, "rol": self.rol}
