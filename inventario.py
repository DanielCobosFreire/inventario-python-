import os

# Clase Producto para representar cada artículo
class Producto:
    def __init__(self, codigo, nombre, cantidad, precio):
        self.codigo = codigo
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def __str__(self):
        return f"{self.codigo},{self.nombre},{self.cantidad},{self.precio}"

    @staticmethod
    def desde_linea(linea):
        try:
            codigo, nombre, cantidad, precio = linea.strip().split(",")
            return Producto(codigo, nombre, int(cantidad), float(precio))
        except ValueError:
            raise ValueError("Error al convertir los datos del archivo. Formato inválido.")

# Clase Inventario con manejo de archivos
class Inventario:
    ARCHIVO = "inventario.txt"

    def __init__(self):
        self.productos = []
        self.cargar_desde_archivo()

    # Cargar inventario desde el archivo
    def cargar_desde_archivo(self):
        if not os.path.exists(self.ARCHIVO):
            open(self.ARCHIVO, "w").close()  # Crear archivo si no existe
            return

        try:
            with open(self.ARCHIVO, "r") as archivo:
                for linea in archivo:
                    if linea.strip():  # Evitar líneas vacías
                        producto = Producto.desde_linea(linea)
                        self.productos.append(producto)
        except FileNotFoundError:
            print("Archivo de inventario no encontrado. Se creará uno nuevo.")
        except PermissionError:
            print("Error: No tienes permisos para leer el archivo de inventario.")
        except Exception as e:
            print(f"Error inesperado al leer el archivo: {e}")

    # Guardar inventario en el archivo
    def guardar_en_archivo(self):
        try:
            with open(self.ARCHIVO, "w") as archivo:
                for producto in self.productos:
                    archivo.write(str(producto) + "\n")
        except PermissionError:
            print("Error: No tienes permisos para escribir en el archivo de inventario.")
        except Exception as e:
            print(f"Error inesperado al guardar el archivo: {e}")

    def agregar_producto(self, producto):
        self.productos.append(producto)
        self.guardar_en_archivo()
        print(f" Producto '{producto.nombre}' agregado correctamente al inventario.")

    def actualizar_producto(self, codigo, cantidad=None, precio=None):
        for producto in self.productos:
            if producto.codigo == codigo:
                if cantidad is not None:
                    producto.cantidad = cantidad
                if precio is not None:
                    producto.precio = precio
                self.guardar_en_archivo()
                print(f" Producto '{producto.nombre}' actualizado correctamente.")
                return
        print(" Producto no encontrado.")

    def eliminar_producto(self, codigo):
        for producto in self.productos:
            if producto.codigo == codigo:
                self.productos.remove(producto)
                self.guardar_en_archivo()
                print(f" Producto '{producto.nombre}' eliminado correctamente.")
                return
        print(" Producto no encontrado.")

    def mostrar_inventario(self):
        if not self.productos:
            print(" El inventario está vacío.")
        else:
            print("\n Inventario actual:")
            for producto in self.productos:
                print(f"Código: {producto.codigo} | Nombre: {producto.nombre} | "
                      f"Cantidad: {producto.cantidad} | Precio: ${producto.precio:.2f}")


# Programa principal con manejo de excepciones
def menu():
    inventario = Inventario()

    while True:
        print("\n--- Menú de Gestión de Inventario ---")
        print("1. Mostrar Inventario")
        print("2. Agregar Producto")
        print("3. Actualizar Producto")
        print("4. Eliminar Producto")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                inventario.mostrar_inventario()
            elif opcion == "2":
                codigo = input("Ingrese código del producto: ")
                nombre = input("Ingrese nombre del producto: ")
                cantidad = int(input("Ingrese cantidad: "))
                precio = float(input("Ingrese precio: "))
                producto = Producto(codigo, nombre, cantidad, precio)
                inventario.agregar_producto(producto)
            elif opcion == "3":
                codigo = input("Ingrese código del producto a actualizar: ")
                cantidad = input("Ingrese nueva cantidad (deje vacío si no desea cambiar): ")
                precio = input("Ingrese nuevo precio (deje vacío si no desea cambiar): ")

                cantidad = int(cantidad) if cantidad else None
                precio = float(precio) if precio else None
                inventario.actualizar_producto(codigo, cantidad, precio)
            elif opcion == "4":
                codigo = input("Ingrese código del producto a eliminar: ")
                inventario.eliminar_producto(codigo)
            elif opcion == "5":
                print(" Saliendo del sistema de inventario...")
                break
            else:
                print(" Opción no válida. Intente de nuevo.")
        except ValueError:
            print(" Error: Ingrese valores numéricos válidos para cantidad y precio.")
        except Exception as e:
            print(f" Error inesperado: {e}")


if __name__ == "__main__":
    menu()
