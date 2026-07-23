# Clases de Dominio (POO)
class Producto:
    def __init__(self, ingrediente, categoria, precio):
        self.ingrediente = ingrediente
        self.categoria = categoria
        self.precio = precio
        self.stock_actual = 0
        self.stock_minimo = 0

    def descontar_stock(self, cantidad):
        """Método POO para actualizar el inventario del objeto"""
        self.stock_actual -= cantidad

    def requiere_reabastecimiento(self):
        """Evalúa si el stock cayó por debajo del umbral"""
        return self.stock_actual < self.stock_minimo

class TransaccionVenta:
    def __init__(self, order_id, cliente_nombre, producto, cantidad, metodo_pago, fecha_hora):
        self.order_id = order_id
        self.cliente_nombre = cliente_nombre
        self.producto = producto  # Recibe un objeto de la clase Producto
        self.cantidad = cantidad
        self.monto_total = cantidad * producto.precio
        self.metodo_pago = metodo_pago
        self.fecha_hora = fecha_hora

class AsientoERP:
    def __init__(self, id_transaccion, fecha, monto, metodo_pago, descripcion):
        self.id_transaccion = id_transaccion
        self.fecha = fecha
        self.monto = monto
        self.metodo_pago = metodo_pago
        self.descripcion = descripcion

class OrdenCompraSCM:
    def __init__(self, fecha, ingrediente, cantidad_solicitada):
        self.fecha = fecha
        self.ingrediente = ingrediente
        self.cantidad_solicitada = cantidad_solicitada
        self.estado = 'Pendiente'