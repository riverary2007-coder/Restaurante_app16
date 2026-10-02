# restaurante_app — Semana 16

## Propósito y evolución

Esta entrega continúa el proyecto gráfico de la Semana 15. Conserva el inicio de sesión, la navegación lateral, la identidad visual y sus recursos de `assets/`, la gestión de productos y el registro de ventas. La sección Usuarios evoluciona para demostrar el manejo de eventos de Tkinter mediante un formulario y un `Treeview`.

## Gestión de usuarios y roles

El modelo `Usuario` incluye el rol **Administrador**, **Empleado** o **Cliente**. La sesión muestra la cuenta y su rol. Solo un Administrador ve y puede abrir la gestión administrativa. Desde esa pantalla puede registrar, consultar, actualizar y eliminar usuarios Empleado y Cliente. La tabla presenta identificación, nombre, usuario y rol; no expone contraseñas. Al seleccionar una fila, el identificador permite recuperar el objeto desde `RestauranteServicio`.

El servicio valida campos, duplicados y roles, actualiza los índices en memoria y persiste los cambios en `datos/usuarios.json`. La interfaz no accede directamente a los archivos JSON. La cuenta Administrador autenticada no puede eliminarse; tampoco se eliminan usuarios con ventas asociadas.

## Eventos y callbacks

- `Treeview.bind("<<TreeviewSelect>>", callback)`: toma el identificador de la fila y carga los datos en el formulario mediante una consulta al servicio.
- `Entry.bind("<Return>", callback)`: activa el registro reutilizando `registrar_usuario()`.
- `Entry.bind("<Escape>", callback)`: limpia campos y cancela la selección.
- `Combobox.bind("<<ComboboxSelected>>", callback)`: responde al cambio de rol y limita las opciones de la interfaz a Empleado y Cliente.
- Los botones Registrar, Actualizar, Eliminar y Limpiar usan `command=`; cada callback coordina la vista y delega las reglas y persistencia al servicio.

## Arquitectura y archivos

```text
restaurante_app/
├── datos/       productos.json, usuarios.json, ventas.json
├── modelos/     producto.py, usuario.py, venta.py
├── servicios/   archivo_servicio.py, restaurante_servicio.py
├── ui/          login_view.py, main_view.py
├── assets/      logo, iconos y recursos visuales
├── main.py
└── README.md
```

`ArchivoServicio` centraliza la lectura y escritura JSON. `RestauranteServicio` contiene las operaciones y validaciones. `LoginView` y `MainView` presentan la aplicación y coordinan la interacción.

## Acceso de prueba

```text
Usuario: ana
Contraseña: 1234
Rol: Administrador
```

Las cuentas de prueba `carlos`, `maria`, `juan` y `sofia` usan la contraseña `1234` y tienen roles Empleado o Cliente.

## Ejecución

Requiere Python 3.10 o superior y Tkinter. Desde la carpeta del proyecto:

```bash
python main.py
```

## Comprobaciones

Se verifican compilación sintáctica de los módulos y operaciones de registro, duplicidad, actualización, consulta por identificador, eliminación, protección de la cuenta autenticada, roles y persistencia en JSON. La interfaz conserva los recursos existentes de `assets/`.
