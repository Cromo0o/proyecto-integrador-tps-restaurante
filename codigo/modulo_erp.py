# Módulo de Caja Financiera - ERP
import pandas as pd

class ModuloERP:
    def __init__(self):
        self.archivo_caja = '../datos/caja_erp.csv'

    def registrar_ingreso(self, asiento):
        """Recibe un objeto AsientoERP directamente"""
        # Convertimos los atributos del objeto en un DataFrame y guardamos
        nueva_transaccion = pd.DataFrame([asiento.__dict__])
        
        nueva_transaccion.to_csv(self.archivo_caja, mode='a', index=False, header=False)
        print(f"✅ [ERP] Ingreso financiero de ${asiento.monto:.2f} registrado en caja.")