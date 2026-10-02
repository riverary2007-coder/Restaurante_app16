class Producto:
    """Modelo de producto del restaurante."""

    def __init__(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int = 0) -> None:
        self.codigo = codigo.strip()
        self.nombre = nombre.strip()
        self.categoria = categoria.strip()
        self.precio = float(precio)
        self.stock = int(stock)
        self._validar()

    def _validar(self) -> None:
        if not self.codigo or not self.nombre or not self.categoria:
            raise ValueError("Código, nombre y categoría son obligatorios.")
        if self.precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo.")

    @classmethod
    def from_dict(cls, datos: dict) -> "Producto":
        return cls(
            str(datos["codigo"]),
            str(datos["nombre"]),
            str(datos["categoria"]),
            float(datos["precio"]),
            int(datos.get("stock", 0)),
        )

    def actualizar(self, nombre: str, categoria: str, precio: float, stock: int) -> None:
        anterior = (self.nombre, self.categoria, self.precio, self.stock)
        self.nombre = nombre.strip()
        self.categoria = categoria.strip()
        self.precio = float(precio)
        self.stock = int(stock)
        try:
            self._validar()
        except Exception:
            self.nombre, self.categoria, self.precio, self.stock = anterior
            raise

    def to_dict(self) -> dict:
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock,
        }

    def __str__(self) -> str:
        return f"{self.codigo} | {self.nombre} | {self.categoria} | ${self.precio:.2f} | Stock: {self.stock}"
