# Punto de Entrada TPS y Core Central
import pandas as pd
import datetime as dt
import os

# Importación de Módulos y Modelos
from modulo_scm import ModuloSCM
from modulo_erp import ModuloERP
from modulo_bi import ModuloBI
from modulo_crm import ModuloCRM
from modelos import Producto, TransaccionVenta, AsientoERP

class RestaurantePOS:

    # Constructor del Sistema Principal para su inicialización y verificación de archivos
    def __init__(self):
        self.nombre = "Cadena de Restaurantes"
        self.scm = ModuloSCM()
        self.erp = ModuloERP()
        self.bi = ModuloBI()
        self.crm = ModuloCRM()
        self.verificar_archivos()

    # Verificación de Archivos y Creación de Estructura Inicial
    def verificar_archivos(self):
        if not os.path.exists('../datos'):
            # Si no existe la carpeta de datos, la creamos
            os.makedirs('../datos')

        if not os.path.exists('../datos/caja_erp.csv'):
            # Si no existe el archivo de caja del ERP, lo creamos con las columnas necesarias
            # Index = false para evitar que Pandas agregue una columna de índice adicional al CSV
            pd.DataFrame(columns=['id_transaccion', 'fecha', 'monto', 'metodo_pago', 'descripcion']).to_csv('../datos/caja_erp.csv', index=False)

        if not os.path.exists('../datos/inventario_scm.csv'):
            # Si no existe el archivo de inventario del SCM, lo creamos con datos iniciales
            # Ponemos la comida que existe el database histórico y su stock actual y mínimo para el sistema de gestión de inventario
            pd.DataFrame({
                'ingrediente': ['Pizza', 'Brownie', 'Fries', 'Burger', 'Cake', 'Salad', 'Pasta', 'Soup', 'Ice Cream'],
                'stock_actual': [50, 15, 60, 40, 20, 30, 25, 20, 35],
                'stock_minimo': [10, 10, 15, 10, 5, 8, 8, 5, 10]
            }).to_csv('../datos/inventario_scm.csv', index=False)
            
        if not os.path.exists('../datos/ordenes_compra.csv'):
            # Si no existe el archivo de órdenes de compra, lo creamos con las columnas necesarias
            pd.DataFrame(columns=['fecha', 'ingrediente', 'cantidad_solicitada', 'estado']).to_csv('../datos/ordenes_compra.csv', index=False)

    # Interfaz de Consola para permitir al usuario interactuar con el sistema, registrando nuevas órdenes de comida y gestionando la integración con los módulos SCM, ERP, BI y CRM
    def iniciar_consola(self):

        while True:
            # Menú Principal del Sistema
            print(f"\n{'='*40}")    # Separador visual
            print(f"   SISTEMA CORE - {self.nombre}   ")
            print(f"{'='*40}")      # Separador visual
            print("1. Registrar nueva orden de comida")
            print("2. Salir del sistema")

            # Solicitamos al usuario que seleccione una opción del menú
            opcion = input("\nSeleccione una opción (1-2): ")

            # Validamos la opción seleccionada y ejecutamos la acción correspondiente
            if opcion == '1':
                self.pantalla_nueva_orden()
            elif opcion == '2':
                print("\nCerrando sistema... ¡Hasta pronto!")
                break
            else:
                print("\nOpción inválida. Intente de nuevo.")

    # Menú para registrar una nueva orden de comida, solicitando al usuario los datos necesarios
    def pantalla_nueva_orden(self):
        print("\n--- NUEVA ORDEN ---")

        # Guardamos el nombre del cliente que realiza la orden
        cliente = input("Nombre del cliente: ")

        # Definimos un diccionario con los platos disponibles, sus categorías y precios
        # La clave es el número de opción, y el valor es una tupla con (nombre del plato, categoría, precio)
        # Con key, el sistema no tiene que recorrer una lista, sino que accede directamente con la key
        menu_items = {
            '1': ('Pizza', 'Main', 12.50), '2': ('Burger', 'Main', 8.50),
            '3': ('Pasta', 'Main', 10.00), '4': ('Salad', 'Starter', 6.00),
            '5': ('Soup', 'Starter', 5.50), '6': ('Fries', 'Starter', 4.00),
            '7': ('Brownie', 'Dessert', 5.00), '8': ('Cake', 'Dessert', 6.50),
            '9': ('Ice Cream', 'Dessert', 4.50)
        }

        # Mostramos el menú de platos disponibles al usuario
        print("\n--- MENÚ DISPONIBLE ---")
        for key, value in menu_items.items():
            # Mostramos el número de opción, el nombre del plato, su precio y su categoría
            print(f"{key}. {value[0]} - ${value[2]:.2f} ({value[1]})")
            
        opcion_plato = input("\nSeleccione el número del plato (1-9): ")

        # Validamos la opción seleccionada
        if opcion_plato in menu_items:
            # 1. POO: Instanciamos el Objeto Producto con sus datos base
            datos_plato = menu_items[opcion_plato]
            producto_seleccionado = Producto(datos_plato[0], datos_plato[1], datos_plato[2])
        else:
            print("Opción inválida. Cancelando orden.")
            return

        # Solicitamos al usuario la cantidad deseada del plato seleccionado
        cantidad = int(input(f"Cantidad de {producto_seleccionado.ingrediente}: "))

        # Solicitamos al usuario que seleccione un método de pago
        print("\n1. Cash  2. Credit Card  3. Debit Card  4. Online Payment")
        opcion_pago = input("Seleccione el método de pago (1-4): ")
        # Definimos un diccionario para mapear la opción de pago a su descripción
        metodos = {'1': 'Cash', '2': 'Credit Card', '3': 'Debit Card', '4': 'Online Payment'}
        # Asigna el método de pago seleccionado, o 'Cash' por defecto si la opción es inválida
        metodo_pago = metodos.get(opcion_pago, 'Cash')

        # 1. Obtenemos la fecha y hora de la última orden registrada en el histórico
        # df_hist es el DataFrame que contiene el histórico de órdenes, y se lee desde un archivo CSV
        df_hist = pd.read_csv('../datos/restaurant_orders.csv')
        # Convertimos la columna 'Order Time' a tipo datetime para poder manipularla correctamente
        df_hist['Order Time'] = pd.to_datetime(df_hist['Order Time'])
        
        # Obtenemos la fecha y hora de la última orden registrada, y le sumamos un día para generar la fecha y hora de la nueva orden
        ultima_fecha = df_hist['Order Time'].max()
        fecha_hora = (ultima_fecha + dt.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')

        # 2. Obtenemos el nuevo ID de orden sumando 1 al máximo ID existente en el histórico
        df_orders = pd.read_csv('../datos/restaurant_orders.csv')
        # Si el DataFrame no está vacío, obtenemos el máximo ID y le sumamos 1; si está vacío, asignamos 1 como nuevo ID
        nuevo_id = df_orders['Order ID'].max() + 1 if not df_orders.empty else 1
        
        # 2. POO: Instanciamos el Objeto TransaccionVenta encapsulando el Producto
        nueva_venta = TransaccionVenta(nuevo_id, cliente, producto_seleccionado, cantidad, metodo_pago, fecha_hora)

        # 3. Procesamos la integración con los módulos SCM, ERP, BI y CRM
        self.procesar_integracion(nueva_venta)

    # "nueva_venta" cambia a nombre a "venta" para que sea más claro y consistente con el resto del código
    def procesar_integracion(self, venta):
        print("\n[SISTEMA] Verificando disponibilidad...")
        
        # 1. ¿Stock Disponible? (Pasamos el objeto Producto al SCM)
        # Llamamos al método "validar_disponibilidad" del módulo SCM, que devuelve un booleano indicando si hay stock y un DataFrame con el inventario actualizado
        hay_stock, df_inv = self.scm.validar_disponibilidad(venta.producto, venta.cantidad)
        if not hay_stock:
            return 
            
        # 2. Genera Registro en restaurant_orders.csv (Extraemos datos del objeto Venta)
        nuevo_pedido = pd.DataFrame([{
            'Order ID': venta.order_id, 'Customer Name': venta.cliente_nombre, 
            'Food Item': venta.producto.ingrediente, 'Category': venta.producto.categoria, 
            'Quantity': venta.cantidad, 'Price': venta.producto.precio, 
            'Payment Method': venta.metodo_pago, 'Order Time': venta.fecha_hora
        }])

        # Guardamos el nuevo pedido en el archivo CSV de órdenes, en modo append (a), sin índice y sin encabezado
        # append (a), conserva los datos existentes y agrega el nuevo pedido al final del archivo, sin sobrescribirlo
        nuevo_pedido.to_csv('../datos/restaurant_orders.csv', mode='a', index=False, header=False)
        print(f"✅ [CORE] Pedido #{venta.order_id} guardado en la base de datos principal.")

        # 3. ERP: Instanciamos un Objeto AsientoERP y se lo pasamos al Módulo ERP
        asiento_financiero = AsientoERP(
            venta.order_id, venta.fecha_hora, venta.monto_total, 
            venta.metodo_pago, f"Venta {venta.cantidad}x {venta.producto.ingrediente}"
        )
        self.erp.registrar_ingreso(asiento_financiero)

        # 4. SCM: Descuento y Validación con el Objeto Producto actualizado
        self.scm.procesar_descuento_y_reabastecimiento(df_inv, venta.producto, venta.cantidad, venta.fecha_hora)

        # 5. BI: Dashboard Analítico
        self.bi.generar_dashboard()

        # 6. CRM: Monitoreo Automatizado de Clientes
        self.crm.evaluar_riesgo_desercion()
        
        print("\n[+] ¡Transacción completada con éxito!")

# Punto de entrada del sistema, donde se instancia la clase RestaurantePOS y se inicia la consola interactiva
# Con esto el programa arranca solo cuando se ejecuta directamente desde el main, y no cuando se importa como módulo en otro script
if __name__ == "__main__":
    sistema = RestaurantePOS()
    sistema.iniciar_consola()