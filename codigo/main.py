# Punto de Entrada TPS y Core Central
import pandas as pd
import datetime as dt
import os

from modulo_scm import ModuloSCM
from modulo_erp import ModuloERP
from modulo_bi import ModuloBI
from modulo_crm import ModuloCRM
from modelos import Producto, TransaccionVenta, AsientoERP

class RestaurantePOS:
    def __init__(self):
        self.nombre = "Cadena de Restaurantes"
        self.scm = ModuloSCM()
        self.erp = ModuloERP()
        self.bi = ModuloBI()
        self.crm = ModuloCRM()
        self.verificar_archivos()

    def verificar_archivos(self):
        if not os.path.exists('../datos'):
            os.makedirs('../datos')

        if not os.path.exists('../datos/caja_erp.csv'):
            pd.DataFrame(columns=['id_transaccion', 'fecha', 'monto', 'metodo_pago', 'descripcion']).to_csv('../datos/caja_erp.csv', index=False)

        if not os.path.exists('../datos/inventario_scm.csv'):
            pd.DataFrame({
                'ingrediente': ['Pizza', 'Brownie', 'Fries', 'Burger', 'Cake', 'Salad', 'Pasta', 'Soup', 'Ice Cream'],
                'stock_actual': [50, 15, 60, 40, 20, 30, 25, 20, 35],
                'stock_minimo': [10, 10, 15, 10, 5, 8, 8, 5, 10]
            }).to_csv('../datos/inventario_scm.csv', index=False)
            
        if not os.path.exists('../datos/ordenes_compra.csv'):
            pd.DataFrame(columns=['fecha', 'ingrediente', 'cantidad_solicitada', 'estado']).to_csv('../datos/ordenes_compra.csv', index=False)

    def iniciar_consola(self):
        while True:
            print(f"\n{'='*40}")
            print(f"   SISTEMA CORE - {self.nombre}   ")
            print(f"{'='*40}")
            print("1. Registrar nueva orden de comida")
            print("2. Salir del sistema")
            
            opcion = input("\nSeleccione una opción (1-2): ")
            
            if opcion == '1':
                self.pantalla_nueva_orden()
            elif opcion == '2':
                print("\nCerrando sistema... ¡Hasta pronto!")
                break
            else:
                print("\nOpción inválida. Intente de nuevo.")

    def pantalla_nueva_orden(self):
        print("\n--- NUEVA ORDEN ---")
        cliente = input("Nombre del cliente: ")
        
        menu_items = {
            '1': ('Pizza', 'Main', 12.50), '2': ('Burger', 'Main', 8.50),
            '3': ('Pasta', 'Main', 10.00), '4': ('Salad', 'Starter', 6.00),
            '5': ('Soup', 'Starter', 5.50), '6': ('Fries', 'Starter', 4.00),
            '7': ('Brownie', 'Dessert', 5.00), '8': ('Cake', 'Dessert', 6.50),
            '9': ('Ice Cream', 'Dessert', 4.50)
        }
        
        print("\n--- MENÚ DISPONIBLE ---")
        for key, value in menu_items.items():
            print(f"{key}. {value[0]} - ${value[2]:.2f} ({value[1]})")
            
        opcion_plato = input("\nSeleccione el número del plato (1-9): ")
        
        if opcion_plato in menu_items:
            # 1. POO: Instanciamos el Objeto Producto con sus datos base
            datos_plato = menu_items[opcion_plato]
            producto_seleccionado = Producto(datos_plato[0], datos_plato[1], datos_plato[2])
        else:
            print("Opción inválida. Cancelando orden.")
            return

        cantidad = int(input(f"Cantidad de {producto_seleccionado.ingrediente}: "))
        
        print("\n1. Cash  2. Credit Card  3. Debit Card  4. Online Payment")
        opcion_pago = input("Seleccione el método de pago (1-4): ")
        metodos = {'1': 'Cash', '2': 'Credit Card', '3': 'Debit Card', '4': 'Online Payment'}
        metodo_pago = metodos.get(opcion_pago, 'Cash')
        
        df_hist = pd.read_csv('../datos/restaurant_orders.csv')
        df_hist['Order Time'] = pd.to_datetime(df_hist['Order Time'])
        ultima_fecha = df_hist['Order Time'].max()
        fecha_hora = (ultima_fecha + dt.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        
        df_orders = pd.read_csv('../datos/restaurant_orders.csv')
        nuevo_id = df_orders['Order ID'].max() + 1 if not df_orders.empty else 1
        
        # 2. POO: Instanciamos el Objeto TransaccionVenta encapsulando el Producto
        nueva_venta = TransaccionVenta(nuevo_id, cliente, producto_seleccionado, cantidad, metodo_pago, fecha_hora)
        
        self.procesar_integracion(nueva_venta)

    def procesar_integracion(self, venta):
        print("\n[SISTEMA] Verificando disponibilidad...")
        
        # 1. ¿Stock Disponible? (Pasamos el objeto Producto al SCM)
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
        self.crm.evaluar_riesgo_desercion() # <-- AGREGAR ESTA LÍNEA
        
        print("\n[+] ¡Transacción completada con éxito!")

if __name__ == "__main__":
    sistema = RestaurantePOS()
    sistema.iniciar_consola()