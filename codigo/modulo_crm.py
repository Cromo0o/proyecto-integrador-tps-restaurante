# Módulo CRM - Gestión de Relación con el Cliente
import pandas as pd
import datetime as dt

class ModuloCRM:
    def __init__(self):
        self.archivo_pedidos = '../datos/restaurant_orders.csv'

    def evaluar_riesgo_desercion(self):
        """Bloque: CRM -> Alerta de Cliente en Riesgo de Deserción"""
        try:
            df = pd.read_csv(self.archivo_pedidos)
            df['Order Time'] = pd.to_datetime(df['Order Time'])
            
            # Calculamos la fecha actual de simulación (la última transacción registrada + 1 día)
            current_date = df['Order Time'].max() + dt.timedelta(days=1)
            
            # Agrupamos por cliente para ver cuántos días han pasado desde su ÚLTIMA compra
            rfm = df.groupby('Customer Name').agg({
                'Order Time': lambda x: (current_date - x.max()).days
            }).rename(columns={'Order Time': 'Recency'})
            
            # Aislamos los registros: Clientes con 60 días o más de inactividad
            clientes_en_riesgo = rfm[rfm['Recency'] >= 60]
            
            if not clientes_en_riesgo.empty:
                print(f"\n⚠️ [CRM - ALERTA AUTOMATIZADA]")
                print(f"Se detectaron {len(clientes_en_riesgo)} cliente(s) en 'Riesgo de Deserción' (>= 60 días de inactividad):")
                for cliente, row in clientes_en_riesgo.iterrows():
                    print(f"   - {cliente}: Aislar registro -> {row['Recency']} días sin compras.")
                print(f"   [!] Acción recomendada: Disparar campaña de retención (Email/Descuento).")
            else:
                print("\n✅ [CRM] Monitoreo completado: Ningún cliente crítico en riesgo de deserción hoy.")
                
        except Exception as e:
            print(f"⚠️ [CRM] No se pudo ejecutar el monitoreo: {e}")