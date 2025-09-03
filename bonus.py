import csv
import os

# Archivos CSV usados por el sistema
ARCHIVO_CLIENTES = "clientes.csv"
ARCHIVO_PRODUCTOS = "productos.csv"
ARCHIVO_VENTAS = "ventas.csv"

# Crea los archivos con encabezados si no existen
def inicializar_archivos():
    if not os.path.exists(ARCHIVO_CLIENTES):
        with open(ARCHIVO_CLIENTES, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'nombre', 'apellido', 'telefono', 'activo'])

    if not os.path.exists(ARCHIVO_PRODUCTOS):
        with open(ARCHIVO_PRODUCTOS, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'nombre', 'precio', 'activo'])

    if not os.path.exists(ARCHIVO_VENTAS):
        with open(ARCHIVO_VENTAS, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id_pedido', 'id_cliente', 'id_producto', 'cantidad', 'activo'])

# Obtiene un nuevo ID secuencial para un archivo dado
def obtener_nuevo_id(archivo, campo_id):
    try:
        with open(archivo, 'r') as f:
            lector = csv.DictReader(f)
            ids = [int(fila[campo_id]) for fila in lector]
            return max(ids) + 1 if ids else 1
    except FileNotFoundError:
        return 1

# -----------------------------------
# CLIENTES
# -----------------------------------

def registrar_cliente():
    print("\n--- Registrar Cliente ---")
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    telefono = input("Teléfono: ").strip()
    nuevo_id = obtener_nuevo_id(ARCHIVO_CLIENTES, 'id')

    with open(ARCHIVO_CLIENTES, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([nuevo_id, nombre, apellido, telefono, 1])
    print(f"Cliente registrado con ID: {nuevo_id}")

def listar_clientes():
    print("\n--- Lista de Clientes ---")
    try:
        with open(ARCHIVO_CLIENTES, 'r') as f:
            lector = csv.DictReader(f)
            vacio = True
            for fila in lector:
                if fila['activo'] == '1':
                    print(f"ID: {fila['id']} - {fila['nombre']} {fila['apellido']} - Tel: {fila['telefono']}")
                    vacio = False
            if vacio:
                print("No hay clientes activos.")
    except FileNotFoundError:
        print("No se encontró el archivo de clientes.")

def eliminar_cliente():
    print("\n--- Eliminar Cliente ---")
    id_buscar = input("Ingrese el ID del cliente a eliminar: ").strip()
    filas_modificadas = []

    try:
        with open(ARCHIVO_CLIENTES, 'r') as f:
            lector = csv.DictReader(f)
            for fila in lector:
                if fila['id'] == id_buscar:
                    fila['activo'] = '0'
                filas_modificadas.append(fila)

        with open(ARCHIVO_CLIENTES, 'w', newline='') as f:
            campos = ['id', 'nombre', 'apellido', 'telefono', 'activo']
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()
            writer.writerows(filas_modificadas)

        print("Cliente eliminado (lógicamente).")
    except FileNotFoundError:
        print("No se encontró el archivo de clientes.")

# -----------------------------------
# PRODUCTOS
# -----------------------------------

def registrar_producto():
    print("\n--- Registrar Producto ---")
    nombre = input("Nombre del producto: ").strip()
    precio = float(input("Precio: ").strip())
    nuevo_id = obtener_nuevo_id(ARCHIVO_PRODUCTOS, 'id')

    with open(ARCHIVO_PRODUCTOS, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([nuevo_id, nombre, precio, 1])
    print(f"Producto registrado con ID: {nuevo_id}")

def listar_productos():
    print("\n--- Lista de Productos ---")
    try:
        with open(ARCHIVO_PRODUCTOS, 'r') as f:
            lector = csv.DictReader(f)
            vacio = True
            for fila in lector:
                if fila['activo'] == '1':
                    print(f"ID: {fila['id']} - {fila['nombre']} - Precio: ${fila['precio']}")
                    vacio = False
            if vacio:
                print("No hay productos activos.")
    except FileNotFoundError:
        print("No se encontró el archivo de productos.")

# -----------------------------------
# VENTAS
# -----------------------------------

def guardar_venta():
    print("\n--- Guardar Venta ---")
    id_cliente = input("ID del cliente: ").strip()

    listar_productos()
    id_producto = input("ID del producto: ").strip()
    cantidad = int(input("Cantidad: ").strip())

    nuevo_id = obtener_nuevo_id(ARCHIVO_VENTAS, 'id_pedido')

    with open(ARCHIVO_VENTAS, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([nuevo_id, id_cliente, id_producto, cantidad, 1])

    print("Venta registrada correctamente.")

def listar_ventas_por_cliente():
    print("\n--- Ventas por Cliente ---")
    nombre_cliente = input("Ingrese el nombre del cliente: ").strip().lower()
    id_cliente = None

    # Buscar cliente por nombre
    try:
        with open(ARCHIVO_CLIENTES, 'r') as f:
            lector = csv.DictReader(f)
            for fila in lector:
                if fila['activo'] == '1' and fila['nombre'].strip().lower() == nombre_cliente:
                    id_cliente = fila['id']
                    break
    except FileNotFoundError:
        print("No se encontró el archivo de clientes.")
        return

    if not id_cliente:
        print("Cliente no encontrado o inactivo.")
        return

    # Cargar productos activos
    productos = {}
    try:
        with open(ARCHIVO_PRODUCTOS, 'r') as f:
            lector = csv.DictReader(f)
            for fila in lector:
                if fila['activo'] == '1':
                    productos[fila['id']] = {
                        'nombre': fila['nombre'],
                        'precio': float(fila['precio'])
                    }
    except FileNotFoundError:
        print("No se encontró el archivo de productos.")
        return

    # Listar ventas del cliente
    total = 0
    try:
        with open(ARCHIVO_VENTAS, 'r') as f:
            lector = csv.DictReader(f)
            print(f"\nVentas de '{nombre_cliente}':")
            for fila in lector:
                if fila['id_cliente'] == id_cliente and fila['activo'] == '1':
                    id_prod = fila['id_producto']
                    if id_prod in productos:
                        nombre = productos[id_prod]['nombre']
                        precio = productos[id_prod]['precio']
                        cantidad = int(fila['cantidad'])
                        subtotal = precio * cantidad
                        print(f"{nombre} - {cantidad} x ${precio:.2f} = ${subtotal:.2f}")
                        total += subtotal
            print(f"Total de ventas: ${total:.2f}")
    except FileNotFoundError:
        print("No se encontró el archivo de ventas.")

# -----------------------------------
# MENÚ PRINCIPAL
# -----------------------------------

def menu():
    inicializar_archivos()

    while True:
        print("\n========= MENÚ PRINCIPAL =========")
        print("1. Registrar cliente")
        print("2. Listar clientes")
        print("3. Eliminar cliente")
        print("4. Registrar producto")
        print("5. Listar productos")
        print("6. Guardar una venta")
        print("7. Listar ventas por cliente")
        print("8. Salir")
        print("==================================")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == '1':
            registrar_cliente()
        elif opcion == '2':
            listar_clientes()
        elif opcion == '3':
            eliminar_cliente()
        elif opcion == '4':
            registrar_producto()
        elif opcion == '5':
            listar_productos()
        elif opcion == '6':
            guardar_venta()
        elif opcion == '7':
            listar_ventas_por_cliente()
        elif opcion == '8':
            print("Programa finalizado.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    menu()
