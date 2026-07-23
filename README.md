# Sistema Transaccional y Analítico Integrado (TPS-SCM-ERP-CRM-BI)

## 📌 Descripción del Proyecto
Este proyecto implementa un **ecosistema de software modular e integrado** desarrollado en Python bajo el paradigma de **Programación Orientada a Objetos (POO)**. Su objetivo es digitalizar y optimizar la gestión operativa y analítica de una cadena de restaurantes, eliminando los silos de información tradicionales mediante una arquitectura orientada a eventos.

El núcleo del sistema es un **Punto de Venta (TPS)** que opera en tiempo real coordinando cuatro módulos satélites automatizados:

* 📦 **SCM (Supply Chain Management):** Realiza el descuento automático de inventario tras cada venta, monitorea el stock mínimo y emite órdenes de compra automatizadas a proveedores si se detecta reabastecimiento.
* 💰 **ERP (Enterprise Resource Planning):** Registra los asientos contables de cada transacción financiera en la caja chica, garantizando la trazabilidad del flujo de caja según el método de pago (Efectivo, Tarjeta de Crédito/Débito, Pago en Línea).
* 👥 **CRM (Customer Relationship Management):** Monitorea la inactividad histórica de los clientes y aísla registros para disparar alertas automatizadas de **Riesgo de Deserción** (clientes con >= 60 días sin realizar compras).
* 📊 **BI (Business Intelligence):** Implementa el algoritmo de **Segmentación RFM** (Recencia, Frecuencia, Valor Monetario) y genera un **Tablero de Control Gerencial** gráfico (`dashboard_gerencial.png`) que consolida la tendencia de ventas semanales, la rotación del menú, los ingresos por método de pago y la distribución de la cartera de clientes.

---

## 🛠️ Tecnologías y Librerías Utilizadas

* **Lenguaje:** Python 3.x
* **Paradigma:** Programación Orientada a Objetos (POO)
* **Librerías Principales:**
  * `pandas`: Procesamiento, manipulación y filtrado eficiente de datos en estructuras `DataFrame`.
  * `matplotlib`: Creación y renderizado automatizado del Dashboard Gerencial en formato de imagen (`.png`).
  * `datetime` / `os` / `sys`: Gestión de marcas de tiempo, rutas del sistema operativo y manejo de archivos.

---

## 🚀 Preparación del Entorno e Instalación

Para probar o ejecutar el sistema en tu equipo local, sigue estos pasos:

### 1. Clonar el Repositorio
```bash
git clone [https://github.com/Cromo0o/proyecto-integrador-tps-restaurante.git](https://github.com/Cromo0o/proyecto-integrador-tps-restaurante.git)
cd proyecto-integrador-tps-restaurante
```

### 2. Crear un Entorno Virtual
Se recomienda utilizar un entorno virtual para aislar las dependencias del proyecto.

* **En Linux / macOS:**
  ```bash
  python3 -m venv venv
  ```
* **En Windows (PowerShell / CMD):**
  ```powershell
  python -m venv venv
  ```

### 3. Activar el Entorno Virtual

* **En Linux / macOS:**
  ```bash
  source venv/bin/activate
  ```
* **En Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
* **En Windows (CMD):**
  ```cmd
  .\venv\Scripts\activate.bat
  ```

*(Verás que el prefijo `(venv)` aparece al inicio de la terminal).*

### 4. Instalar Dependencias
Instala todas las librerías necesarias ejecutando:

```bash
pip install -r requirements.txt
```

---

## 🎮 Ejecución del Sistema

Una vez configurado el entorno virtual e instaladas las dependencias:

1. Navega a la carpeta de código:
   ```bash
   cd codigo
   ```

2. Ejecuta el script principal:
   ```bash
   python main.py
   ```

3. **Simulación de Orden:**
   * Selecciona la opción `1. Registrar nueva orden de comida`.
   * Ingresa el nombre del cliente.
   * Selecciona el platillo del menú y la cantidad deseada.
   * Elige el método de pago.
   * Observa en tiempo real cómo la consola despliega los eventos automáticos hacia el **ERP**, **SCM**, **BI** y **CRM**.
   * Revisa la carpeta `datos/` para verificar cómo se actualizaron los archivos `.csv` y el gráfico `dashboard_gerencial.png`.

---

## 📂 Estructura del Repositorio

```text
SISTEMA_POS_RESTAURANTE/
├── .gitignore          # Reglas de exclusión para Git (omite venv/ y temporales)
├── README.md           # Documentación del proyecto
├── requirements.txt    # Archivo de dependencias del proyecto
├── codigo/
│   ├── main.py         # Orquestador principal e interfaz de consola POS (TPS)
│   ├── modelos.py      # Clases POO (Producto, TransaccionVenta, etc.)
│   ├── modulo_bi.py    # Módulo de Inteligencia de Negocios y Segmentación RFM
│   ├── modulo_crm.py   # Monitoreo de clientes y alertas de deserción
│   ├── modulo_erp.py   # Asientos contables y gestión de caja chica
│   └── modulo_scm.py   # Gestión de inventario y órdenes de compra automáticas
├── datos/
│   ├── caja_erp.csv            # Libro contable de ingresos
│   ├── dashboard_gerencial.png # Tablero de control generado dinámicamente
│   ├── inventario_scm.csv      # Control de insumos y stock
│   ├── ordenes_compra.csv      # Registro de reabastecimiento a proveedores
│   └── restaurant_orders.csv   # Base de datos histórica de ventas
└── Diagrama de Flujo/
    └── Diagrama de Flujo del Sistema.png # Diagrama de arquitectura del flujo
```

---

## 👨‍💻 Información Académica

* **Autor:** Matthew Llerena Montoya
* **Institución:** Escuela Politécnica Nacional
* **Materia:** Sistemas de la Información
