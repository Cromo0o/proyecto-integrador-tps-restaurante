# Control de Inventario y Abastecimiento - SCM
import pandas as pd
from modelos import OrdenCompraSCM

class ModuloSCM:
    def __init__(self):
        self.archivo_inv = '../datos/inventario_scm.csv'
        self.archivo_oc = '../datos/ordenes_compra.csv'

    def validar_disponibilidad(self, producto, cantidad):
        """Recibe un objeto Producto y carga su stock desde la base"""
        df_inv = pd.read_csv(self.archivo_inv)
        idx_producto = df_inv.index[df_inv['ingrediente'] == producto.ingrediente].tolist()
        
        if not idx_producto:
            print(f"❌ [ERROR] El producto '{producto.ingrediente}' no existe en el inventario.")
            return False, None

        idx = idx_producto[0]
        # Cargamos los datos del CSV al Objeto
        producto.stock_actual = df_inv.at[idx, 'stock_actual']
        producto.stock_minimo = df_inv.at[idx, 'stock_minimo']
        
        if cantidad > producto.stock_actual:
            print(f"❌ [ALERTA SCM] Transacción denegada. Solo quedan {producto.stock_actual} unidades de '{producto.ingrediente}'.")
            return False, None
            
        return True, df_inv

    def procesar_descuento_y_reabastecimiento(self, df_inv, producto, cantidad, fecha_hora):
        idx = df_inv.index[df_inv['ingrediente'] == producto.ingrediente].tolist()[0]
        
        # Uso de POO: El objeto descuenta su propio stock
        producto.descontar_stock(cantidad)
        
        # Guardamos el nuevo estado del objeto en el DataFrame
        df_inv.at[idx, 'stock_actual'] = producto.stock_actual
        df_inv.to_csv(self.archivo_inv, index=False)
        print(f"✅ [SCM] Stock de '{producto.ingrediente}' actualizado. Quedan {producto.stock_actual} unidades.")
        
        # Uso de POO: El objeto evalúa si necesita reabastecerse
        if producto.requiere_reabastecimiento():
            print(f"⚠️ [SCM - ALERTA] ¡Stock bajo detectado para '{producto.ingrediente}'!")
            
            # Instanciamos una Orden de Compra como objeto
            orden = OrdenCompraSCM(fecha_hora, producto.ingrediente, 20)
            nueva_orden = pd.DataFrame([orden.__dict__]) # Convierte el objeto a formato tabla automáticamente
            
            nueva_orden.to_csv(self.archivo_oc, mode='a', index=False, header=False)
            print(f"✅ [SCM] Orden de compra automática generada para el proveedor.")