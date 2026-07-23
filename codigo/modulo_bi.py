# Inteligencia de Negocios (BI) - Módulo de Análisis y Visualización de Datos
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

class ModuloBI:
    def generar_dashboard(self):
        """Bloque: BI Dashboard Analítico -> Clasifica Cliente RFM y Actualiza Gráficos"""
        try:
            df = pd.read_csv('../datos/restaurant_orders.csv')
            df['Order Time'] = pd.to_datetime(df['Order Time'])
            df['Total_Amount'] = df['Quantity'] * df['Price']

            # Algoritmo RFM
            current_date = df['Order Time'].max() + dt.timedelta(days=1)
            rfm = df.groupby('Customer Name').agg({
                'Order Time': lambda x: (current_date - x.max()).days,
                'Order ID': 'count',
                'Total_Amount': 'sum'
            }).rename(columns={'Order Time': 'Recency', 'Order ID': 'Frequency', 'Total_Amount': 'Monetary'})

            def segmentar(row):
                if row['Frequency'] > 1: return 'VIP'
                if row['Recency'] < 60: return 'Activo'
                if row['Recency'] < 120: return 'En Riesgo'
                return 'Recuperable'

            rfm['Segmento'] = rfm.apply(segmentar, axis=1)

            # Graficar
            plt.style.use('ggplot')
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            fig.suptitle('Dashboard Gerencial - Cadena de Restaurantes', fontsize=16, fontweight='bold')

            weekly_sales = df.set_index('Order Time').resample('W')['Total_Amount'].sum()
            semanas_secuenciales = list(range(1, len(weekly_sales) + 1))
            axes[0, 0].plot(semanas_secuenciales, weekly_sales.values, marker='o', color='#2b5c8f', linewidth=2)
            axes[0, 0].set_title('Evolución de Ventas Semanal')
            axes[0, 0].set_xlabel('Semana #')
            axes[0, 0].set_ylabel('Ventas ($)')
            axes[0, 0].xaxis.set_major_locator(MultipleLocator(5))
            axes[0, 0].xaxis.set_minor_locator(MultipleLocator(1))
            axes[0, 0].grid(True, which='major', axis='x', color='white', linewidth=1.5)
            axes[0, 0].grid(True, which='minor', axis='x', color='white', linewidth=0.7)
            axes[0, 0].grid(True, axis='y', color='white', linewidth=1.5)

            segments = rfm['Segmento'].value_counts()
            axes[0, 1].pie(segments, labels=segments.index, autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
            axes[0, 1].set_title('Segmentación de Clientes (RFM)')

            items_sold = df.groupby('Food Item')['Quantity'].sum().sort_values(ascending=True)
            axes[1, 0].barh(items_sold.index, items_sold.values, color='#e07a5f')
            axes[1, 0].set_title('Demanda de Productos / Insumos (SCM)')
            axes[1, 0].set_xlabel('Unidades Vendidas')

            payments = df.groupby('Payment Method')['Total_Amount'].sum()
            axes[1, 1].bar(payments.index, payments.values, color='#81b29a')
            axes[1, 1].set_title('Ingresos Financieros por Método de Pago (ERP)')
            axes[1, 1].set_ylabel('Ingresos ($)')

            plt.tight_layout()
            plt.savefig('../datos/dashboard_gerencial.png') 
            plt.close() 
            print("📊 [BI] Dashboard actualizado en '../datos/dashboard_gerencial.png'.")
        except Exception as e:
            print(f"⚠️ [BI] No se pudo actualizar el dashboard: {e}")