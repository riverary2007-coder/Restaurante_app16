from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class RestauranteServicio:
    """Centraliza validaciones, operaciones del restaurante y persistencia."""

    def __init__(
        self,
        registros_productos: list[dict],
        registros_usuarios: list[dict],
        registros_ventas: list[dict] | None = None,
        archivo_servicio=None,
    ) -> None:
        self._productos: list[Producto] = []
        self._usuarios: list[Usuario] = []
        self._ventas: list[Venta] = []
        self._productos_por_codigo: dict[str, Producto] = {}
        self._usuarios_por_nombre: dict[str, Usuario] = {}
        self._usuarios_por_identificacion: dict[str, Usuario] = {}
        self._archivo_servicio = archivo_servicio

        self._cargar_productos(registros_productos)
        self._cargar_usuarios(registros_usuarios)
        self._cargar_ventas(registros_ventas or [])

    def _cargar_productos(self, registros: list[dict]) -> None:
        for registro in registros:
            try:
                producto = Producto.from_dict(registro)
                clave = producto.codigo.lower()
                if clave not in self._productos_por_codigo:
                    self._productos.append(producto)
                    self._productos_por_codigo[clave] = producto
            except (KeyError, TypeError, ValueError):
                continue

    def _cargar_usuarios(self, registros: list[dict]) -> None:
        for registro in registros:
            try:
                usuario = Usuario.from_dict(registro)
                clave = usuario.usuario.lower()
                if clave not in self._usuarios_por_nombre:
                    self._usuarios.append(usuario)
                    self._usuarios_por_nombre[clave] = usuario
                    self._usuarios_por_identificacion[usuario.identificacion.lower()] = usuario
            except (KeyError, TypeError, ValueError):
                continue

    def _cargar_ventas(self, registros: list[dict]) -> None:
        for registro in registros:
            try:
                venta = Venta.from_dict(registro)
                if self.buscar_usuario_por_identificacion(venta.usuario_id) and self.buscar_producto(venta.producto_codigo):
                    self._ventas.append(venta)
            except (KeyError, TypeError, ValueError):
                continue

    # ---------- ACCESO ----------
    def validar_acceso(self, usuario: str, contrasena: str) -> bool:
        registro = self._usuarios_por_nombre.get(usuario.strip().lower())
        return registro is not None and registro.contrasena == contrasena

    # ---------- USUARIOS ----------
    def listar_usuarios(self) -> list[Usuario]:
        return self._usuarios.copy()

    def cantidad_usuarios(self) -> int:
        return len(self._usuarios)

    def buscar_usuario(self, usuario: str) -> Usuario | None:
        return self._usuarios_por_nombre.get(usuario.strip().lower())

    def buscar_usuario_por_identificacion(self, identificacion: str) -> Usuario | None:
        return self._usuarios_por_identificacion.get(identificacion.strip().lower())

    def registrar_usuario(self, identificacion: str, nombre: str, correo: str, usuario: str,
                         contrasena: str, rol: str) -> tuple[bool, str]:
        identificacion, usuario = identificacion.strip(), usuario.strip()
        if not all((identificacion, nombre.strip(), correo.strip(), usuario, contrasena)):
            return False, "Complete todos los campos del usuario."
        if identificacion.lower() in self._usuarios_por_identificacion:
            return False, "No se puede registrar: la identificación ya existe."
        if usuario.lower() in self._usuarios_por_nombre:
            return False, "No se puede registrar: el nombre de usuario ya existe."
        if rol not in ("Empleado", "Cliente"):
            return False, "Solo se pueden registrar usuarios Empleado o Cliente."
        try:
            nuevo = Usuario(identificacion, nombre, correo, usuario, contrasena, rol)
            self._usuarios.append(nuevo)
            self._usuarios_por_nombre[usuario.lower()] = nuevo
            self._usuarios_por_identificacion[identificacion.lower()] = nuevo
            self._guardar_usuarios()
        except (ValueError, TypeError, OSError, RuntimeError) as error:
            if 'nuevo' in locals() and nuevo in self._usuarios:
                self._usuarios.remove(nuevo)
                self._usuarios_por_nombre.pop(usuario.lower(), None)
                self._usuarios_por_identificacion.pop(identificacion.lower(), None)
            return False, f"No se pudo registrar el usuario: {error}"
        return True, "Usuario registrado correctamente."

    def actualizar_usuario(self, identificacion: str, nombre: str, correo: str,
                           usuario: str, contrasena: str, rol: str) -> tuple[bool, str]:
        actual = self.buscar_usuario_por_identificacion(identificacion)
        if actual is None:
            return False, "Usuario no encontrado."
        if not all((nombre.strip(), correo.strip(), usuario.strip(), contrasena)):
            return False, "Complete todos los campos del usuario."
        if rol not in ("Empleado", "Cliente"):
            return False, "Solo se pueden asignar los roles Empleado o Cliente."
        otro = self._usuarios_por_nombre.get(usuario.strip().lower())
        if otro is not None and otro is not actual:
            return False, "Ese nombre de usuario ya está registrado."
        previo = (actual.nombre, actual.correo, actual.usuario, actual.contrasena, actual.rol)
        self._usuarios_por_nombre.pop(actual.usuario.lower(), None)
        actual.nombre, actual.correo = nombre.strip(), correo.strip()
        actual.usuario, actual.contrasena, actual.rol = usuario.strip(), contrasena, rol
        self._usuarios_por_nombre[actual.usuario.lower()] = actual
        try:
            self._guardar_usuarios()
        except (OSError, RuntimeError) as error:
            self._usuarios_por_nombre.pop(actual.usuario.lower(), None)
            actual.nombre, actual.correo, actual.usuario, actual.contrasena, actual.rol = previo
            self._usuarios_por_nombre[actual.usuario.lower()] = actual
            return False, f"No se pudo actualizar el usuario: {error}"
        return True, "Usuario actualizado correctamente."

    def eliminar_usuario(self, identificacion: str, identificacion_autenticada: str) -> tuple[bool, str]:
        usuario = self.buscar_usuario_por_identificacion(identificacion)
        if usuario is None:
            return False, "Usuario no encontrado."
        if usuario.identificacion.lower() == identificacion_autenticada.strip().lower():
            return False, "No puede eliminar la cuenta administrativa actualmente autenticada."
        if any(v.usuario_id.lower() == usuario.identificacion.lower() for v in self._ventas):
            return False, "No se puede eliminar: el usuario tiene ventas asociadas."
        self._usuarios.remove(usuario)
        self._usuarios_por_nombre.pop(usuario.usuario.lower(), None)
        self._usuarios_por_identificacion.pop(usuario.identificacion.lower(), None)
        try:
            self._guardar_usuarios()
        except (OSError, RuntimeError) as error:
            self._usuarios.append(usuario)
            self._usuarios_por_nombre[usuario.usuario.lower()] = usuario
            self._usuarios_por_identificacion[usuario.identificacion.lower()] = usuario
            return False, f"No se pudo eliminar el usuario: {error}"
        return True, "Usuario eliminado correctamente."

    # ---------- PRODUCTOS ----------
    def listar_productos(self) -> list[Producto]:
        return self._productos.copy()

    def cantidad_productos(self) -> int:
        return len(self._productos)

    def buscar_producto(self, codigo: str) -> Producto | None:
        return self._productos_por_codigo.get(codigo.strip().lower())

    def registrar_producto(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int) -> tuple[bool, str]:
        codigo = codigo.strip()
        if not codigo:
            return False, "El código es obligatorio."
        if codigo.lower() in self._productos_por_codigo:
            return False, "No se puede registrar: el código ya existe."
        try:
            producto = Producto(codigo, nombre, categoria, precio, stock)
        except (ValueError, TypeError) as error:
            return False, str(error)
        self._productos.append(producto)
        self._productos_por_codigo[codigo.lower()] = producto
        self._guardar_productos()
        return True, "Producto registrado correctamente."

    def cargar_producto(self, codigo: str) -> Producto | None:
        return self.buscar_producto(codigo)

    def actualizar_producto(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int) -> tuple[bool, str]:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False, "Producto no encontrado."
        try:
            producto.actualizar(nombre, categoria, precio, stock)
        except (ValueError, TypeError) as error:
            return False, str(error)
        self._guardar_productos()
        return True, "Producto actualizado correctamente."

    def eliminar_producto(self, codigo: str) -> tuple[bool, str]:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False, "Producto no encontrado."

        codigo_normalizado = codigo.strip().lower()
        if any(
            venta.producto_codigo.strip().lower() == codigo_normalizado
            for venta in self._ventas
        ):
            return False, "No se puede eliminar: el producto tiene ventas asociadas."

        self._productos.remove(producto)
        self._productos_por_codigo.pop(codigo_normalizado, None)
        self._guardar_productos()
        return True, "Producto eliminado correctamente."

    # ---------- VENTAS ----------
    def registrar_venta(self, identificacion_usuario: str, codigo_producto: str) -> tuple[bool, str, Venta | None]:
        usuario = self.buscar_usuario_por_identificacion(identificacion_usuario)
        if usuario is None:
            return False, "No se puede registrar la venta: el usuario no existe.", None

        producto = self.buscar_producto(codigo_producto)
        if producto is None:
            return False, "No se puede registrar la venta: el producto no existe.", None

        try:
            venta = Venta(usuario.identificacion, producto.codigo)
        except (ValueError, TypeError) as error:
            return False, str(error), None

        self._ventas.append(venta)
        try:
            self._guardar_ventas()
        except Exception as error:
            self._ventas.pop()
            return False, f"No se pudo guardar la venta: {error}", None

        return True, "Venta registrada correctamente.", venta

    def listar_ventas(self) -> list[Venta]:
        return self._ventas.copy()

    def cantidad_ventas(self) -> int:
        return len(self._ventas)

    def _guardar_productos(self) -> None:
        if self._archivo_servicio is None:
            raise RuntimeError("No existe un servicio de archivos configurado.")
        self._archivo_servicio.guardar_productos([p.to_dict() for p in self._productos])

    def _guardar_usuarios(self) -> None:
        if self._archivo_servicio is None:
            raise RuntimeError("No existe un servicio de archivos configurado.")
        self._archivo_servicio.guardar_usuarios([u.to_dict() for u in self._usuarios])

    def _guardar_ventas(self) -> None:
        if self._archivo_servicio is None:
            raise RuntimeError("No existe un servicio de archivos configurado.")
        self._archivo_servicio.guardar_ventas([v.to_dict() for v in self._ventas])
