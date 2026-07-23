# Inteligencia de Negocios (BI) - Módulo de Análisis y Visualización de Datos
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

class ModuloBI:
    def generar_dashboard(self):
        # Bloque: BI Dashboard Analítico -> Clasifica Cliente RFM y Actualiza Gráficos
        try:
            df = pd.read_csv('../datos/restaurant_orders.csv')
            df['Order Time'] = pd.to_datetime(df['Order Time'])
            # Crea una nueva columna calculando el ingreso por cada línea (Cantidad x Precio)
            df['Total_Amount'] = df['Quantity'] * df['Price']

            # Algoritmo RFM (Recencia, Frecuencia, Valor Monetario)
            # Avanza el reloj 1 día respecto a la venta más reciente para usarlo como el "Hoy" virtual
            current_date = df['Order Time'].max() + dt.timedelta(days=1)

            # Agrupamos por cliente para calcular sus 3 métricas
            rfm = df.groupby('Customer Name').agg({
                'Order Time': lambda x: (current_date - x.max()).days,  # R: Días desde su última compra
                'Order ID': 'count',                                    # F: Cantidad total de pedidos que ha hecho
                'Total_Amount': 'sum'                                   # M: Todo el dinero que ha gastado
            }).rename(columns={'Order Time': 'Recency', 'Order ID': 'Frequency', 'Total_Amount': 'Monetary'})

            # Función para etiquetar a los clientes según su comportamiento
            def segmentar(row):
                # Si un cliente ha hecho más de 1 compra, es VIP
                # Si su última compra fue hace menos de 60 días, es Activo
                # Si fue hace menos de 120 días, está En Riesgo; de lo contrario
                # Recuperable; perdimos ese cliente por lo que toca ver la forma de recuperarlo dando algun tipo de incentivo fuerte
                if row['Frequency'] > 1: return 'VIP'
                if row['Recency'] < 60: return 'Activo'
                if row['Recency'] < 120: return 'En Riesgo'
                return 'Recuperable'

            # Aplica la función fila por fila (axis=1) para crear la nueva columna 'Segmento'
            # apply es como un bucle super rapido y optimizado
            # La función segmentar se aplica a cada fila del DataFrame rfm, y el resultado se almacena en la nueva columna 'Segmento'.
            # axis = 1 recorre la tabla de izquierda a derecha (fila por fila)
            # axis = 0 recorre la tabla de arriba a abajo (columna por columna)
            rfm['Segmento'] = rfm.apply(segmentar, axis=1)

            # Graficar

            # Aplicamos un estilo visual predefinido para que los gráficos luzcan más modernos
            plt.style.use('ggplot')

            # Cramos la figura (fig) y la cuadrícula de 2x2 (axes). figsize define el tamaño en pulgadas.
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            fig.suptitle('Dashboard Gerencial - Cadena de Restaurantes', fontsize=16, fontweight='bold')

            # ==========================
            # GRÁFICO 1: Línea de tiempo
            # ==========================
            weekly_sales = df.set_index('Order Time').resample('W')['Total_Amount'].sum()
            semanas_secuenciales = list(range(1, len(weekly_sales) + 1))

            # Dibuja la línea con los datos de ventas semanales, marcadores en cada punto, color azul oscuro y grosor de línea 2
            axes[0, 0].plot(semanas_secuenciales, weekly_sales.values, marker='o', color='#2b5c8f', linewidth=2)
            axes[0, 0].set_title('Evolución de Ventas Semanal')
            axes[0, 0].set_xlabel('Semana #')
            axes[0, 0].set_ylabel('Ventas ($)')

            # Personaliza la rejilla de fondo para mejorar la legibilidad del gráfico
            axes[0, 0].xaxis.set_major_locator(MultipleLocator(5))
            axes[0, 0].xaxis.set_minor_locator(MultipleLocator(1))
            axes[0, 0].grid(True, which='major', axis='x', color='white', linewidth=1.5)
            axes[0, 0].grid(True, which='minor', axis='x', color='white', linewidth=0.7)
            axes[0, 0].grid(True, axis='y', color='white', linewidth=1.5)

            # =================
            # GRÁFICO 2: Pastel
            # =================
            
            # Contamos cuántos clientes hay en cada segmento para el gráfico de pastel
            segments = rfm['Segmento'].value_counts()

            """Dibujamos el gráfico de pastel con los segmentos de clientes, 
            mostrando el porcentaje (autopct) de cada segmento 
            y usando colores personalizados"""
            axes[0, 1].pie(segments, labels=segments.index, autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
            axes[0, 1].set_title('Segmentación de Clientes (RFM)')

            # ==============================
            # GRÁFICO 3: Barras Horizontales
            # ==============================

            # Agrupamos por nombre del plato, sumamos las cantidades y las ordenamos para el gráfico
            items_sold = df.groupby('Food Item')['Quantity'].sum().sort_values(ascending=True)

            # barch() crea barras horizontales con los datos de productos vendidos, usando un color personalizado
            axes[1, 0].barh(items_sold.index, items_sold.values, color='#e07a5f')
            axes[1, 0].set_title('Demanda de Productos / Insumos (SCM)')
            axes[1, 0].set_xlabel('Unidades Vendidas')

            # ============================
            # GRÁFICO 4: Barras Verticales
            # ============================
            
            # Agrupamos por método de pago y sumamos los ingresos totales para cada método
            payments = df.groupby('Payment Method')['Total_Amount'].sum()

            # bar() crea barras verticales con los datos de ingresos por método de pago, usando un color personalizado
            axes[1, 1].bar(payments.index, payments.values, color='#81b29a')
            axes[1, 1].set_title('Ingresos Financieros por Método de Pago (ERP)')
            axes[1, 1].set_ylabel('Ingresos ($)')

            # =========================
            # 4. EXPORTACIÓN Y LIMPIEZA
            # =========================

            # Ajusta automáticamente los márgenes para que los títulos y ejes no se monten unos sobre otros
            plt.tight_layout()

            # Guarda la imagen final generada directamente en la carpeta de datos  
            plt.savefig('../datos/dashboard_gerencial.png') 

            # Cierra la figura en memoria RAM para evitar fugas de memoria, ya que no se mostrará en pantalla
            plt.close() 
            print("📊 [BI] Dashboard actualizado en '../datos/dashboard_gerencial.png'.")
        except Exception as e:
            # Si un CSV falta o hay un error, lo atrapa y avisa sin que el programa completo se caiga
            print(f"⚠️ [BI] No se pudo actualizar el dashboard: {e}")